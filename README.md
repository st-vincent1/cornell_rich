# Cornell-rich

Cornell-rich is a set of rich character (and film) annotations for another open-source corpus of film dialogue. 
The corpus contains annotations for almost 600 movies, with a total of 863 speakers utterring up to 145K lines of the [Cornell Movie Dialog Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html).

## Data Format

The corpus is provided in a comma-separated value (CSV) format with the following columns:

- **name**: character's name
- **movie_title**: title of the movie
- **number_of_lines**: number of lines spoken by the given character in the corpus
- **age_bracket**: the age category of the character
- **profession**: profession of the character (if any)
- **religion**: religion of the character (if any)
- **country_of_origin**: country of origin of the character
- **additional_info**: any additional information about the character, such as trivia or who played them
- **quote**: a characteristic quote of the character
- **annotated**: whether the character was considered for annotations
- **speaker_id**: ID of the speaker
- **movie_id**: ID of the movie
- **gender**: gender of the speaker
- **description**: character description for the speaker
- **source**: where the information was sourced

## Extraction

To extract the dataset from scratch, you can run the following script:

```
bash src/download_cornell_base.sh
python src/create_cornell_rich.py
```

## Paper

If you use Cornell-rich in your research, please cite the following paper:

[Vincent et al. 2023, Personalised Language Modelling of Screen Characters Using Rich Metadata Annotations. arXiv.](https://arxiv.org/abs/2303.16618)

## Contact

For any questions or comments, please raise an Issue within this repository.
