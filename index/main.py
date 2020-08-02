#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import sys
import argparse
import traceback
import re
import glob
import elasticsearch
from elasticsearch import helpers

client = elasticsearch.Elasticsearch("localhost:9200")


def main():
    encode = "utf-8"
    dirs = glob.glob("../wikipedia-articles/*")
    for d in dirs:
        print(d)
        files = glob.glob(d+"/*")
        for input_path in files:
            print(input_path)

            # read content
            with codecs.open(input_path, "r", encode) as f:
                lines = f.readlines()

            id = ""
            url = ""
            title = ""
            content = ""
            start_content = False
            skip_line = False
            for line in lines:
                out_text = line.rstrip("\n")
                m = re.match(
                    r'<doc id="(.+)" url="(.+)" title="(.+)">', out_text)
                if m is not None:
                    id = m.group(1)
                    url = m.group(2)
                    title = m.group(3)
                    start_content = True
                    skip_line = True
                elif re.match(r'</doc>', out_text) is not None:
                    print("{0} {1} {2}".format(id, url, title.encode('utf-8')))

                    doc = {}
                    doc['id'] = id
                    doc['url'] = url
                    doc['title'] = title
                    doc['content'] = content

                    client.index(index='wikipda', doc_type='_doc', body=doc)

                    id = ""
                    url = ""
                    title = ""
                    content = ""
                    start_content = False
                    skip_line = False
                else:
                    if start_content is True and skip_line is False:
                        content += out_text

                    if skip_line is True:
                        skip_line = False


if __name__ == '__main__':
    main()
