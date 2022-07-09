#!/usr/bin/env python3

# File: recipes.py

import requests

page = requests.get('file:///home/alex/Git/Jeff/Recipes/Tzouhalem.html')
contents = page.content

