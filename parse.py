#!/usr/bin/env python3

# File: parse.py

import os
import sys
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
        if tag == 'h1':
            self.show_datum = True
#           for attr in attrs:
#               if 'class' in attr:
#                   print("     attr:", attr)
        if tag == 'h3':
            self.show_datum = True
#           for attr in attrs:
#               if 'content' in attr:
#                   print("     attr:", attr)
        if tag == 'li':
            self.show_datum = True
#           for attr in attrs:
#               if 'content' in attr:
#                   print("     attr:", attr)
    def handle_endtag(self, tag):
        pass
#       print("End tag  :", tag)
    def handle_data(self, data):
        datum = data.strip()
        if datum and self.show_datum:
#           print("Data     :", datum)
            self.data.append(datum)
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

def get_file_name():
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        f = "test.html"
    return f

def get_page(file_name):
    with open(file_name, "br") as infile:
#       page = infile.read()
        page = infile.read().decode("utf-16")
#   encoding = chardet.detect(page)
#   print("Encoding is '{}'.".format(encoding))
#   page = page.decode(encoding['encoding'])
#   page = page.decode("utf-16")
    return page

def parse_a_single_file(file_name, show=False):
    """
    Returns a list consisting of:
    1. name of the drink
    2. listing of ingredients (quantities & instructions included.)
    If <show> is True: prints to the screen as well.
    """
    parser = MyHTMLParser()
    parser.feed(get_page(file_name))
#   print("Here's the output...\n")
#   print("\tDrink: {}".format(parser.data[0]))
    drink = parser.data[0]
    ingredients = parser.data[2:]
    ret = [drink, ingredients]
    if show:
        print(parser.data[0])
#       print("\t{}".format(parser.data[1]))
        for ingredient in ingredients:
            print("  {}".format(ingredient))
    return ret

def remove_parens(source):
    """
    Accepts a string and returns a list of words
    without any that were in parens.
    """
    ret = []
    source_listing = source.split()
    include = True
    for item in source_listing:
        if item.startswith("("):
            include = False
        if include:
            ret.append(item)
        if item.endswith(")"):
            include = True
    return ret

def select_out_ingredient(ingredient, recipes=None):
    """
    Attempts to removes quantities, instructions, etc
    and leave only the name of the ingredient.
    """
    content = remove_parens(ingredient)
    res = []
    for item in content:
        if (not any(c.isdigit() for c in item)
            and not item in {"few", "oz",
                "heaping", "Heaping", "Bar", "bar",
                "Spoon", "spoon",
                "muddle", "Muddle", "Muddled", "muddled", 
                "light", "Light", "a", "of", "at", "end",
                "dashes", "Dashes", "dash", "Dash",
                "Drizzle", "drizzle", "Fresh", "fresh",
                "sectioned", "Sectioned", "section", "Section",
                "Small", "small", "Garnish", "garnish",
                "Piece", "piece", "splash", "Splash",
                "Drops", "drops", "Drop", "drop",
                }):
            res.append(item)
    return ' '.join(res)

def collect_all_ingredients(parent_dir):
    ret = set()
    for f in os.listdir(parent_dir):
        parsed = parse_a_single_file(
            os.path.join(parent_dir, f))
#       print(parsed)
        if parsed[0] in parsed[1]:
            assert False
        ingredients = parsed[1]
        selected = [select_out_ingredient(ingredient)
            for ingredient in ingredients]
        ret.update(selected) 
    return ret

parse_a_single_file(get_file_name(), show=True )
print(parse_a_single_file(get_file_name()))

listing = collect_all_ingredients("Recipes")
print('\n'.join(listing))



