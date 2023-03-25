# Cornell-rich

Cornell-rich is a set of rich character (and film) annotations for another open-source corpus of film dialogue. 
The corpus contains annotations for almost 600 movies, with a total of 863 speakers utterring up to 145K lines and [NUMBER OF TOKENS] tokens.

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
python extract.py --corpus_path <path_to_dialogue_corpus> --output_path <output_path>
```


where `<path_to_dialogue_corpus>` is the path to the original dialogue corpus, and `<output_path>` is the path to the directory where the extracted annotations will be stored.

## Download

Alternatively, you can download the prepared dataset by running the following command:

```
wget https://example.com/xyz-corpus.zip
unzip xyz-corpus.zip
```


## License

The Cornell-rich corpus is released under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/).

## Paper

If you use Cornell-rich in your research, please cite the following paper:

> AUTHOR(S). "TITLE." *JOURNAL/CONFERENCE*, YEAR.

## Contact

For any questions or comments, please contact sebastian.tate.vincent@gmail.com.
