#!/bin/bash
cd quizScatterer/classes/gensimModel
if [ $? != 0 ]; then
  exit 255
fi
rm -f *
wget https://dl.dropboxusercontent.com/s/j75s0eq4eeuyt5n/jawiki.doc2vec.dbow300d.tar.bz2
tar jxvf jawiki.doc2vec.dbow300d.tar.bz2
rm jawiki.doc2vec.dbow300d.tar.bz2
exit 0
