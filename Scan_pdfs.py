#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os
import regex
import glob
import multiprocessing as mp
import importlib

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


# In[11]:


import timing
importlib.reload(timing)
import timing


# In[13]:


@timing.time_log()
def images_to_strings(x):
    """
    """
    
    return {
        nombre: pool.map(pytesseract.image_to_string, archivo) for nombre, archivo in x.items()
    }


# In[2]:


path = os.path.abspath('analisis_clinicos/')
path


# In[3]:


caminos = glob.glob(f"{path}/*.pdf")
caminos


# In[4]:


archivos = [ os.path.split(camino)[1] for camino in caminos]
archivos


# In[5]:


#pool.close()
#pool.terminate()


# In[6]:


pool = mp.Pool()


# In[7]:


imagenes = pool.map(convert_from_path, caminos)


# In[8]:


archivos_en_imagenes = {
    archivo: imagen for archivo, imagen in zip(archivos, imagenes)
}


# In[9]:


archivos_en_imagenes[archivos[0]]


# In[64]:


strings = {
    nombre: pool.map(pytesseract.image_to_string, archivo) for nombre, archivo in archivos_en_imagenes.items()
}


# In[14]:


strings = images_to_strings(archivos_en_imagenes)


# In[15]:


# Sent all of these files to texts/
for nombre, hojas in strings.items():
    for i, hoja in enumerate(hojas):
        _file_name = f"{nombre.replace('.pdf', '')}.{i}.txt"
        with open(_file_name, "w") as f:
                  f.write(hoja)


# In[16]:


for lista in strings.values():
    for string in lista:
        print(regex.findall(r"\d\d.\d\d.\d\d\d\d", string))


# In[43]:


_file = archivos[1]
#print(_file)
print(strings[_file][0])


# In[48]:


_file = archivos[3]
print(_file)
foo = strings[_file][0]
# Split by line breaks :
foo_lines = foo.split("\n")
# Select valid lines (i.e. lionge than 5 characters) :
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


# In[19]:


#print(foo)


# In[44]:


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


# In[41]:


for line in foo_lines:
    for i in regex.finditer(r"^([A-Z\s|[A-Z]\.?)+?(?=(\..+))", line): # FIND lines starting with Caps 
        print(i.string)
        print('\t',i.group())
        for j in regex.finditer(r"(\d+\.\d+|\d+)", i.string): # find groups of numbers
            print(2*'\t',j.group())
            # (?<=\[).+?(?=\])
        for k in regex.finditer(r"(?<=(\d+\.\d+|\d+))\D[^\d]+?(?=\s)", i.string):
            print(3*'\t',k.group())
    #for i in regex.finditer(r"^[A-Z\s]+?(?=(\..+))", line): 


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




