#!/bin/sh

wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2

cd wikiextractor
python setup.py install
cd ..
python wikiextractor/WikiExtractor.py -o wikipedia-articles jawiki-latest-pages-articles.xml.bz2
