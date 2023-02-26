#!/usr/bin/env python
import sys
import string
import tarfile
import gzip
import re
from afinn import Afinn

def clean_text(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub('[\d\n]', ' ', text)
    return text

def mapper():
    afinn = Afinn()
    for line in sys.stdin:
        line = line.strip()
        file_name, file_contents = line.split('\t', 1)
        total_valence = 0
        with tarfile.open(file_contents, 'r:gz') as tar:
            for member in tar.getmembers():
                if member.name.endswith('.txt'):
                    with tar.extractfile(member) as f:
                        content = f.read().decode('utf-8').lower()
                        clean_content = clean_text(content)
                        valence = afinn().score(clean_content)
                        total_valence += valence
            president_name = file_name.split("_")[0]
            print(f"{president_name}\t{total_valence}")

if __name__ == '__main__':
    mapper()