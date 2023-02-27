#!/bin/bash

wget http://www.mpi-sws.org/~cristian/data/cornell_movie_dialogs_corpus.zip

unzip cornell_movie_dialogs_corpus.zip
rm -rf __MACOSX

mv "cornell movie-dialogs corpus" cornell_movie_dialogs_corpus
rm cornell_movie_dialogs_corpus.zip
