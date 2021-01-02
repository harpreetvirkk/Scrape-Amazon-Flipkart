import pandas as pd
import math
import json
import jsonlines
import urllib.parse
import re

# This file splits breadcrumbs and extract the one up category as generic keyword and the last (subsubsubsubcategory) as specific keyword and outputs two 
# files, each containing specific and generic keywords respectively.

# Change path to point to a .jsonl file from where you want to extract the keywords
filepath = './../DATASET/ProductPages/SCRAPED_PRODUCT_PAGES_CLOUDTAIL_TOP_BRANDS.jsonl'

KEYWORDS_file = open(filepath, 'r')

KEYWORDS_List = []
reader = jsonlines.Reader(KEYWORDS_file)
for item in reader.iter():
    KEYWORDS_List.append(item)

df = pd.DataFrame(KEYWORDS_List)

k = list(df['Breadcrumbs'][:])
for i in range(len(k)):
    if type(k[i]) == float: # If breadcrumbs is none
        if math.isnan(k[i]):
            continue
    else:
        if k[i] is not None: # Else split
            if '>' in k[i]:
                k[i] = list(k[i].split('> '))
            elif '›' in k[i]:
                k[i] = list(k[i].split('› '))

generic = []
specific = []
for i in range(len(k)):
    if type(k[i]) == float:
        if math.isnan(k[i]):
            continue
    else:
        if k[i] is not None:
            g = k[i][-2] # Generic is one up
            s = k[i][-1] # Specific is last
            generic.append(g)
            specific.append(s)
print('Total Generic: ',len(generic))
generic = set(generic)
print('Total UNIQUE Generic: ',len(generic))
print('Total Specific: ',len(generic))
specific = set(specific)
print('Total UNIQUE Specific: ',len(generic))
with open ('generic_keywords.txt', 'w') as gen:
    for i in generic:
        # print(i)
        i = re.sub(r'\s\([\,\d]*\)', '', i)
        print(i)
        i = i[:-1]
        i = urllib.parse.quote(i)
        print(i)
        gen.write(i+ '\n')
with open ('specific_keywords.txt', 'w') as spe:
    for i in specific:
        i = re.sub(r'\s\([\,\d]*\)', '', i)
        i = i.replace('\n', '')
        i = urllib.parse.quote(i)
        spe.write(i+ '\n')