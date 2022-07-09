#!/usr/bin/env python3

#File: count.py

"""
Count the number of recipes.
"""
import os

d = 'Recipes'
count = 0 
for f in os.listdir(path=d):
    count += 1
f = "There are {} recipes."
if count > 300:
    f =  "There are {} recipes!"
print(f.format(count))
