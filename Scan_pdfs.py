#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import regex
import glob
import multiprocessing as mp
import importlib
#import pprint

from functools import partial, reduce

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from pdf2image import convert_from_path, convert_from_bytes
import matplotlib.pyplot as plt
import cv2 as cv
import pytesseract


# In[2]:


import timing
importlib.reload(timing)
import timing


# In[3]:


@timing.time_log()
def images_to_strings(x):
    """
    """
    
    return {
        nombre: pool.map(pytesseract.image_to_string, archivo) for nombre, archivo in x.items()
    }


# In[4]:


path = os.path.abspath('analisis_clinicos/')
path


# In[5]:


path_textos = os.path.abspath('textos')
path_textos


# In[13]:


caminos_textos = glob.glob(f"{path_textos}/*.txt")
caminos_textos.sort()
#caminos_textos


# In[14]:


caminos = glob.glob(f"{path}/*.pdf")
#caminos


# In[15]:


archivos = [ os.path.split(camino)[1] for camino in caminos]
archivos


# In[17]:


nombres = [ archivo.replace('.pdf', '') for archivo in archivos ]
nombres


# In[18]:


ahora_si = { 
    archivo: glob.glob(os.path.join(path_textos ,f"{nombre}.?.txt")) 
    for archivo, nombre in zip(archivos, nombres)
}


# In[23]:


[ ahora_si[key].sort() for key in ahora_si.keys() ]
#ahora_si


# In[24]:


Pats = True

if Pats:
    strings = {}
    for key in ahora_si.keys():
        _strings = []
        for _file in ahora_si[key]:
            with open(_file, 'r') as f:
              _strings.append(f.read())
        strings.update({
            key: _strings
        })


# In[30]:


#print(strings[archivos[1]][1])


# In[70]:


#pool.close()
#pool.terminate()


# In[71]:


pool = mp.Pool()


# In[72]:


imagenes = pool.map(convert_from_path, caminos)


# In[73]:


archivos_en_imagenes = {
    archivo: imagen for archivo, imagen in zip(archivos, imagenes)
}


# In[74]:


archivos_en_imagenes[archivos[0]]


# In[77]:


strings2 = {
    nombre: pool.map(pytesseract.image_to_string, archivo) for nombre, archivo in archivos_en_imagenes.items()
}


# In[76]:


strings = images_to_strings(archivos_en_imagenes)


# In[ ]:





# In[106]:


# Send all of these files to texts/

for nombre, hojas in strings.items():
    for i, hoja in enumerate(hojas):
        _file_name = os.path.join(path_textos, f"{nombre.replace('.pdf', '')}.{i}.txt")
        with open(_file_name, "w") as f:
                  f.write(hoja)


# In[ ]:





# In[82]:


for lista in strings.values():
    for string in lista:
        print(regex.findall(r"\d{2}/\d{2}/\d{4}", string))


# In[124]:


_file = archivos[1]
print(_file)
print(len(strings[_file]))
print(strings[_file][2])


# In[101]:


foo = strings[_file][2]

# Split by line breaks :
foo_lines = foo.split("\n")

# Select valid lines (i.e. longer than 5 characters) :
foo_lines = [ line for line in foo_lines ] # if len(line) > 1 ]

#regex.compile(r'[A-Z]')
print(foo_lines[10])
print(foo_lines[14])
"""
for line in foo_lines:
    for i in regex.finditer(r"[0a-z]{2,}", line):
        print(foo_lines[14])
        #print(i.string)
        #print('\t', i.group())
"""


# In[102]:


#print(foo)


# In[103]:


for line in foo_lines:
    for i in regex.finditer(r"^([A-Z\s]|[A-Z]\.?)+?(?=(\..+))", line): # FIND lines starting with Caps 
        print(i.string)
        print('\t',i.group())
        for j in regex.finditer(r"(\d+\.\d+|\d+)", i.string): # find groups of numbers
            print(2*'\t',j.group())
        for k in regex.finditer(r"(?<=(\d+\.\d+|\d+))\D[^\d]+?(?=\s)", i.string):
            print(3*'\t',k.group())
        #for l in regex.finditer(r"()[\d]", i.string):
            #print(4*"\t", l.group())
    #for i in regex.finditer(r"^[A-Z\s]+?(?=(\..+))", line): 


# In[ ]:


"""
for line in foo_lines:
    for i in regex.finditer(r"^([A-Z\s]|[A-Z]\.?)+?(?=(\..+))", line): # FIND lines starting with Caps 
        print(i.string)
        print('\t',i.group())
        for j in regex.finditer(r"(\d+\.\d+|\d+)", i.string): # find groups of numbers
            print(2*'\t',j.group())
        for k in regex.finditer(r"(?<=(\d+\.\d+|\d+))\D[^\d]+?(?=\s)", i.string):
            print(3*'\t',k.group())
"""


# In[43]:


# My regexps :

my_may_ge_2 = r"^[A-Z]{2,}"  # Find CAPITAL WORDS longer than 2, at the begining of the line.
my_numbers = r"(\d+\.\d+|\d+)" # Find numbers of any length, with a decimal point or not.
my_from_begining_until_point = r"^.+?(?=(\..+))" # Find any text before the first occurrence of a pint
my_caps_and_whitespace_until_point = r"^[A-Z\s]+?(?=(\..+))"
my_caps_and_whitspace_or_acronym_until_point = r"^([A-Z\s|[A-Z]\.?)+?(?=(\..+))"
my_failed_extract_units = r"(?<=((\d+\.\d+|\d+)+))(.+)"
googled_text_between_brackets = r"(?<=\[).+?(?=\])"
my_extract_units = r"(?<=(\d+\.\d+|\d+))\D+?(?=(\d+\.\d+|\d+))"
my_better_extract_units_between_numbers = r"(?<=(\d+\.\d+|\d+))\D[^\.\d]+?(?=(\d+\.\d+|\d+))"
my_extract_units_between_numbers_and_whitespace = r"(?<=(\d+\.\d+|\d+))\D[^\.\d]+?(?=\s)"


# In[35]:


dir(regex)
help(regex.purge)


# In[221]:


for line in foo_lines:
    for i in regex.findall(r"^[A-Z]{2,}", line):
        print(i)


# In[152]:


dir(i)


# In[161]:


i.expand()


# In[129]:


help(regex.compile)


# In[128]:


regex.compile()


# In[93]:


[
    reduce(lambda x, y: x + y if y.isupper() else x, line, '')
    for line in woo
]


# In[95]:


#dir('')


# In[101]:


x = "\n hola \n"


# In[103]:


r"{}".format(x)


# In[99]:


print(r'\n\nhola')


# In[74]:


with open('watever', 'w') as lol:
    lol.write(strings[archivos[2]][0])


# In[75]:


# Cuántas líneas tenemos en total :
caracteres_por_linea = pd.core.series.Series(
    [
     len(line) for line in page.split('\n') 
     for pdf in strings 
     for page in pdf
    ],
    name='caracteres'
)


# In[76]:


sns.distplot(caracteres)


# In[36]:


archivos[0]


# In[ ]:





# In[34]:


if False:
    for pdf in strings:
        for page in pdf:
            print(page)


# In[ ]:




