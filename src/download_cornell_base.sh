#!/bin/bash

set -e

curl -OL https://www.mpi-sws.org/~cristian/data/cornell_movie_dialogs_corpus.zip

unzip cornell_movie_dialogs_corpus.zip

mv "cornell movie-dialogs corpus" cornell_movie_dialogs_corpus
rm -r cornell_movie_dialogs_corpus.zip __MACOSX
