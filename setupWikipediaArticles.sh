#!/bin/sh

wget https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2
python -m wikiextractor.WikiExtractor -o wikipedia-articles jawiki-latest-pages-articles.xml.bz2
