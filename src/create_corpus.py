from tqdm import tqdm
import numpy as np
import pandas as pd
import requests
import re
from mosestokenizer import MosesDetokenizer, MosesPunctuationNormalizer
import re
import os

np.random.seed(1)

detokenize = MosesDetokenizer('en')
normalize = MosesPunctuationNormalizer('en')


def preprocess(utterance: str) -> str:
    # Tokenize and detokenize with Moses to make punctuation consistent
    if utterance == '':
        return utterance
    c = normalize(detokenize(normalize(detokenize(utterance.split())).split()))
    c = re.sub(r"I'magine", "Imagine", c)
    c = re.sub(r"\.\.\.\.+", "...", c)
    c = re.sub(r"\.\.\.(\w)", r"... \1", c)
    c = re.sub(r"(\w|)--(\w)", r"\1 -- \2", c)
    c = re.sub("y'knowwhatI'msayin'", "y'know what I'm sayin'", c)
    c = re.sub("That'swhatI'msayin'", "That's what I'm sayin'", c)
    c = re.sub(r"That'swhatI'mtalkin( \"|\" |')bout", "That's what I'm talkin' bout", c)
    # Optional: remove emphasis? Expressed with html, e.g. <u>your</u>, <i>your</i> or <b>your</b>
    c = re.sub(r"</?([uiUIb])>", r"", c)
    c = re.sub("", "--", c)

    return c


def sort_characters_by_lines(corpus):
    characters = {}
    corpus['speaker+title+year'] = '@' + corpus['speaker_name'] + '|' + corpus['title'] + '@' + corpus['year'] + '@'
    for idx, row in tqdm(corpus.iterrows()):
        if pd.isna(row['speaker+title+year']):
            continue
        if row['speaker+title+year'] is not None and not re.findall('@\|', row['speaker+title']):
            try:
                characters[row['speaker+title+year']] += 1
            except KeyError:
                characters[row['speaker+title+year']] = 1
    print(characters)

    speakers, titles, lines = [], [], []
    for k, v in characters.items():
        speaker, title = k[1:-1].split('|')
        lines_ = v
        speakers.append(speaker)
        titles.append(title)
        lines.append(lines_)

    characters = pd.DataFrame({'speakers': speakers,
                               'titles': titles,
                               'lines': lines})
    characters.sort_values(by=['lines'], ascending=False, inplace=True)
    print(characters)
    characters.to_excel('out/sorted_characters.xlsx')


def get_context_by_name(title, year=None):
    base_url = 'http://www.omdbapi.com/?apikey=fa755615&'
    title = re.sub(' ', '+', title)
    req = f"{base_url}t={title}"
    if year:
        req += f"&y={year}"

    try:
        response = requests.get(req).json()
    except (requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError) as e:
        print("Requester error.")
        return {}
    if response["Response"] != "False":
        response = {k: v for k, v in response.items() if v not in ["N/A", "Not rated", "Not Rated", "Unrated"]}
        context = {
            "rated": f"PG rating: {response['Rated']}" if 'Rated' in response.keys() else "",
            "year_of_release": f"Released in {response['Year']}" if 'Year' in response.keys() else "",
            "genre": response["Genre"] if 'Genre' in response.keys() else "",
            "plot": response["Plot"] if 'Plot' in response.keys() else "",
            "country": response["Country"] if 'Country' in response.keys() else "",
            "writers": f"Written by: {response['Writer']}" if 'Writer' in response.keys() else "",
        }

        return context
    return {}


def get_context_by_id(id, char_data):
    # match id to speaker_id
    data = char_data[char_data['speaker_id'] == id]
    if data.empty:
        return {}
    else:
        return {
            "name": data['name'].values[0],
            "age_bracket": data['age_bracket'].values[0],
            "profession": data['profession'].values[0],
            "description": data['description'].values[0],
            "quote": data['quote'].values[0],
            "religion": data['religion'].values[0],
            "country_of_origin": data['country_of_origin'].values[0],
            "gender": data['gender'].values[0],
            "annotated": data['annotated'].values[0],
            "additional_info": data['additional_info'].values[0],
        }


def extract_corpus():
    title_years = []
    utterances = []
    speaker_ids = []
    spoken_to_ids = []

    id = 0
    for index, row in tqdm(movie_conv.iterrows()):
        id += 1
        line_list = row['LineList']
        line_list = re.findall(r'\'\s*([^\']*?)\s*\'', line_list)

        title = film_data[film_data['No'] == row['Film']]['Title'].values[0]
        year = film_data[film_data['No'] == row['Film']]['Year'].values[0]
        title_year = f"{title}_{year}"

        for idx, line in enumerate(line_list):
            try:
                utterance = movie_lines[movie_lines['No'] == line]['Line'].values[0]
            except IndexError:
                continue
            if utterance == '':
                continue

            speaker_label = 'User1' if (idx % 2 == 0) else 'User2'
            spoken_to_label = 'User2' if speaker_label == 'User1' else 'User1'

            speaker_ids.append(row[speaker_label])
            spoken_to_ids.append(row[spoken_to_label])
            utterances.append(utterance)
            title_years.append(title_year)
    corpus = pd.DataFrame({
        'title_year': title_years,
        'utterance': utterances,
        'speaker_id': speaker_ids,
        'spoken_to_id': spoken_to_ids
    })
    return corpus


if __name__ == '__main__':

    # dataset = pd.read_csv("cornell_movie_dialogs_corpus/movie_conversations.txt", delimiter="\t", header=None)
    #
    # # Map film numbers to film metadata
    # film_data = pd.read_csv("cornell_movie_dialogs_corpus/movie_titles_metadata.txt", delimiter="\t",
    #                         encoding="ISO-8859-1", header=None)
    # film_data[['No', 'Title', 'Year', 'IMDB_Rating', 'IMDB_Votes', 'Genres']] = film_data[0].str.split(
    #     r'\+\+\+\$\+\+\+',
    #     expand=True)
    # film_data = film_data[['No', 'Title', 'Year']]
    # film_data = film_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    #
    # # Movie character numbers mapped to character names; normally the code below would be used but we use the
    # # Cornell-rich version instead
    # # char_data = pd.read_csv("cornell_movie_dialogs_corpus/movie_characters_metadata.txt", delimiter="\t",
    # #                         encoding="ISO-8859-1", on_bad_lines='skip', header=None)
    # # char_data[['No', 'Name', 'Film', 'Title', 'Gender', 'Order']] = char_data[0].str.split(r'\+\+\+\$\+\+\+',
    # #                                                                                        expand=True)
    # # char_data = char_data[['No', 'Name', 'Film', 'Title', 'Gender', 'Order']]
    # # char_data = char_data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    #
    # char_data = pd.read_csv("data/cornell_rich_speaker.csv", delimiter=",", on_bad_lines='skip')
    #
    # # Collecting unseen speakers
    # lines_to_find = 5000
    # unseen_characters_ids = []
    # while lines_to_find > 0:
    #     # randomly sample a character from char_data, but only from those field with character description
    #     random_char = char_data[~char_data["description"].isna()].sample(n=1)
    #     if random_char['speaker_id'].values[0] in unseen_characters_ids:
    #         continue
    #     # get the number of lines spoken by the character
    #     lines_to_find -= random_char['number_of_lines'].values[0]
    #     unseen_characters_ids.append(random_char['speaker_id'].values[0])
    #
    # char_data = char_data.drop(columns=['number_of_lines'])
    #
    # # Movie lines structure: [number] [spokesperson] [utterance] from movie_lines.txt
    # movie_lines = pd.read_csv("cornell_movie_dialogs_corpus/movie_lines.txt", delimiter="\t", encoding="ISO-8859-1",
    #                           on_bad_lines='skip', header=None)
    # movie_lines[['No', 'User', 'Film', 'Name', 'Line']] = movie_lines[0].str.split(r'\+\+\+\$\+\+\+', expand=True)
    # movie_lines = movie_lines[['No', 'User', 'Film', 'Name', 'Line']]
    # # Delete whats between [brackets]
    # movie_lines = movie_lines.apply(lambda x: re.sub('\[.*\]', '', x) if x.dtype == 'str' else x)
    # movie_lines = movie_lines.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    #
    # movie_conv = pd.read_csv("cornell_movie_dialogs_corpus/movie_conversations.txt", delimiter="\t",
    #                          encoding="ISO-8859-1", header=None)
    # movie_conv[['User1', 'User2', 'Film', 'LineList']] = movie_conv[0].str.split(r'\+\+\+\$\+\+\+', expand=True)
    # movie_conv = movie_conv[['User1', 'User2', 'Film', 'LineList']]
    # movie_conv = movie_conv.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    #
    # corpus = extract_corpus()
    #
    # # Add title metadata
    # titles = list(set(list(corpus.title_year)))
    # for title in tqdm(titles):
    #     context = get_context_by_name(*title.split('_'))
    #     if context:
    #         for k, v in context.items():
    #             corpus.loc[corpus['title_year'] == title, k] = v
    #
    # speaker_ids = list(set(list(corpus.speaker_id)))
    # for speaker_id in tqdm(speaker_ids):
    #     context = get_context_by_id(speaker_id, char_data)
    #     if context:
    #         for k, v in context.items():
    #             corpus.loc[corpus['speaker_id'] == speaker_id, f"{k}.speaker"] = v
    #
    # spoken_to_ids = list(set(list(corpus.spoken_to_id)))
    # for spoken_to_id in tqdm(spoken_to_ids):
    #     context = get_context_by_id(spoken_to_id, char_data)
    #     if context:
    #         for k, v in context.items():
    #             corpus.loc[corpus['spoken_to_id'] == spoken_to_id, f"{k}.spoken_to"] = v
    #
    # # Preprocess utterances
    # corpus['utterance'] = corpus['utterance'].apply(preprocess)
    #
    # # Split into train, dev, test-common and test-unseen
    # # test-unseen: this corpus contains lines spoken by unseen_characters
    # test_unseen = corpus[corpus['speaker_id'].isin(unseen_characters_ids)]
    # corpus.drop(test_unseen.index, inplace=True)
    # # test-common, valid: randomly sample 10000 lines from the rest of the corpus, then split between them two
    # test_and_valid = corpus[
    #     (~corpus['speaker_id'].isin(unseen_characters_ids)) & corpus['annotated.speaker'] == True].sample(n=10000)
    # test_common = test_and_valid.sample(n=5000)
    # valid = test_and_valid.drop(test_common.index)
    # # train: the rest of the corpus
    # train = corpus.drop(test_and_valid.index)
    #
    # train.to_csv('data/cornell_rich_train.csv', index=False)
    # valid.to_csv('data/cornell_rich_valid.csv', index=False)
    # test_common.to_csv('data/cornell_rich_test_common.csv', index=False)
    # test_unseen.to_csv('data/cornell_rich_test_unseen.csv', index=False)

    train = pd.read_csv('data/cornell_rich_train.csv')
    valid = pd.read_csv('data/cornell_rich_valid.csv')
    test_common = pd.read_csv('data/cornell_rich_test_common.csv')
    test_unseen = pd.read_csv('data/cornell_rich_test_unseen.csv')

    if not os.path.exists("cornell_rich"):
        os.makedirs("cornell_rich")
    if not os.path.exists("cornell_rich/context"):
        os.makedirs("cornell_rich/context")
    for split_set in ['train', 'valid', 'test_common', 'test_unseen']:
        c = pd.read_csv(f'data/cornell_rich_{split_set}.csv')
        # Replace nans with empty strings
        c = c.fillna('')
        for col in c.columns:

            if col in ['title_year', 'spoken_to_id', 'speaker_id', 'annotated.speaker', 'annotated.spoken_to',
                       'name.speaker', 'name.spoken_to']:
                continue
            data = c[col].tolist()
            filename = f"cornell_rich/context/{split_set}.{col}" if col != "utterance" else f"cornell_rich/{split_set}.en"
            if not filename.endswith(".speaker") and not filename.endswith(".spoken_to") and not filename.endswith(
                    ".en"):
                filename += ".meta"
            with open(filename, 'w+') as f:
                for line in data:
                    line = re.sub('Unknown', '', line)
                    f.write(repr(line)[1:-1] + "\n")
