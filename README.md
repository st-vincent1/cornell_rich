# Cornell-rich

Cornell-rich is a set of rich character (and film) annotations for another open-source corpus of film dialogue. 
The corpus contains annotations for almost 600 movies, with a total of 863 speakers utterring up to 145K lines of the 
[Cornell Movie Dialog Corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html).

Details regarding the corpus as well as our experiments in using it for personalised language modelling and evaluation 
of context specificity in machine translation can be found in [our paper](https://arxiv.org/abs/2303.16618).
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

To extract the dataset from scratch:
1. Install dependencies:
`pip install numpy pandas tqdm mosestokenizer`.
2. Download the base Cornell Movie Dialog Corpus: `bash src/download_cornell_base.sh`.
3. Obtain Cornell-rich:
   1. [OPTION 1] Download from [here](https://drive.google.com/drive/folders/13mf6D4wXWZ6rUBx1SQ_xW4btiqUyy0Ei?usp=sharing).
   2. [OPTION 2] Recreate from scratch: `python src/preprocess_and_split.py`. Note that the result of this operation is identical to OPTION 1 and might take a while. The code is mainly provided for reproducibility and transparency.
4. Map the annotations to the base dataset: `python src/create_annotated_corpus.py`.

## Paper

If you use Cornell-rich in your research, please cite the following paper:

[Vincent et al. 2024, Reference-less Analysis of Context Specificity in Translation with Personalised Language Models. arXiv.](https://arxiv.org/abs/2303.16618)

(LREC-COLING 2024 citation will be added once Proceedings are live.)

## Contact

For any questions or comments, please raise an Issue within this repository.
