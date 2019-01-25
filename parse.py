#!/usr/bin/env python3

# File: recipies.py

import os
import urllib
import chardet
from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.data = []
        self.show_datum = False
        super(MyHTMLParser, self).__init__()
    def handle_starttag(self, tag, attrs):
#       print("Start tag:", tag)
        if tag == 'h3':
            self.show_datum = True
            for attr in attrs:
                if 'content' in attr:
                    print("     attr:", attr)
        if tag == 'li':
            self.show_datum = True
            for attr in attrs:
                if 'content' in attr:
                    print("     attr:", attr)
    def handle_endtag(self, tag):
        pass
#       print("End tag  :", tag)
    def handle_data(self, data):
        datum = data.strip()
        if datum and self.show_datum:
            print("Data     :", datum)
        self.show_datum = False
    def handle_comment(self, data):
        print("Comment  :", data)
    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        print("Named ent:", c)
    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        print("Num ent  :", c)
    def handle_decl(self, data):
        print("Decl     :", data)
    def handle_data(self, data):
        datum = data.strip()
        if self.show_datum:
            self.data.append(datum)
            print("Data: ", data)
#           self.show_datum = False
d = 'Recipies'
count = 0 
for f in os.listdir(path=d):
    count += 1
f = "There are {} recipies."
if count > 300:
    f =  "There are {} recipies!"
print(f.format(count))

f = "Recipies/#18.html"
with open(f, "br") as infile:
    page = infile.read()
encoding = chardet.detect(page)
print("Encoding is '{}'.".format(encoding))
page = page.decode(encoding['encoding'])

parser = MyHTMLParser()
parser.feed(page)


