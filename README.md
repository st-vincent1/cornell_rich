# Cornell-rich

Cornell-rich is a set of rich character (and film) annotations for another open-source corpus of film dialogue. 
The corpus contains annotations for almost 600 movies, with a total of 863 speakers utterring up to 145K lines of the [Cornell Movie Dialog Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html).

## Data Format

The corpus is provided in a comma-separated value (CSV) format with the following columns:

- **movie_id**: ID of the movie in the original dialogue corpus
- **line_id**: ID of the line in the original dialogue corpus
- **character**: name of the character speaking the line
- **character_gender**: gender of the character speaking the line
- **character_type**: type of the character (e.g., protagonist, antagonist, supporting)
- **movie_title**: title of the movie
- **year**: year of the movie
- **genre**: genre of the movie
- **line_text**: text of the line spoken by the character

An example file with sample annotations can be found in the `example.tsv` file.

## Extraction

To extract the dataset from scratch, you can run the following script:

```
bash src/download_cornell_base.sh
python src/create_cornell_rich.py
```

## Download

Alternatively, you can download the prepared dataset by running the following command:

```
wget https://example.com/xyz-corpus.zip
unzip xyz-corpus.zip
```

## Paper

If you use Cornell-rich in your research, please cite the following paper:

[Vincent et al. 2023, Personalised Language Modelling of Screen Characters Using Rich Metadata Annotations. arXiv.](https://arxiv.org/abs/2303.16618)

## Contact

For any questions or comments, please raise an Issue within this repository.
