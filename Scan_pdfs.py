#!/usr/bin/env python
# coding: utf-8

# In[37]:


import os
import regex
import glob
import multiprocessing as mp
import importlib
#import pprint

from typing import Tuple, Callable, Any, NoReturn, List, Dict

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


# In[47]:


@timing.time_log()
def images_to_strings(x):
    """
    """
    
    return {
        nombre: pool.map(pytesseract.image_to_string, archivo) for nombre, archivo in x.items()
    }
##

@timing.time_log()
def tab_by_regex(x: str) -> str:
    """
    """
    
    newline = lambda x: f"{x}\n"
    ntab    = lambda n, txt: n*"\t" + txt
    
    _x_lines: List[str] = x.split('\n')
    _my_str:  str       = ''
        
    for line in _x_lines:
        # Match lines starting with Caps, separated by spaces or points : 
        for i in regex.finditer(r"^([A-Z\s]|[A-Z]\.?)+?(?=(\..+))", line): 
            _my_str += newline(i.string)
            _my_str += newline(ntab(1, i.group()))
            # Match numbers, which could be either integers or floats : 
            for j in regex.finditer(r"(\d+\.\d+|\d+)", i.string): # find groups of numbers
                _my_str += newline(ntab(2, j.group()))
            # Match strings found between numbers :
            for k in regex.finditer(r"(?<=(\d+\.\d+|\d+))\D[^\d]+?(?=\s)", i.string):
                _my_str += newline(ntab(3, k.group()))
    
    return _my_str
##

@timing.time_log()
def save_results(x: Dict[str, List[str]]):
    """
        
    """
    
    try:
        if 'segmented' not in os.listdir('.'):
            os.mkdir('segmented')
        
        _camino_resultados = os.path.abspath('segmented')
        _archivos =  list(x.keys())
    
        for i, archivo in enumerate(_archivos):
            for j, page in enumerate(x[archivo]):
                with open(os.path.join(_camino_resultados, f"{_archivos[i].replace('.pdf', '')}.{j+1}.txt"), 'w') as f:
                    f.write(tab_by_regex(page))
    
        return True
    except:
        return False
##


# In[4]:


path = os.path.abspath('analisis_clinicos/')
path


# In[5]:


path_textos = os.path.abspath('textos')
path_textos


# In[6]:


caminos_textos = glob.glob(f"{path_textos}/*.txt")
caminos_textos.sort()
#caminos_textos


# In[7]:


caminos = glob.glob(f"{path}/*.pdf")
#caminos


# In[19]:


archivos = [ os.path.split(camino)[1] for camino in caminos]
archivos


# In[9]:


nombres = [ archivo.replace('.pdf', '') for archivo in archivos ]
nombres


# In[10]:


ahora_si = { 
    archivo: glob.glob(os.path.join(path_textos ,f"{nombre}.?.txt")) 
    for archivo, nombre in zip(archivos, nombres)
}


# In[11]:


[ ahora_si[key].sort() for key in ahora_si.keys() ]
#ahora_si


# In[12]:


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


# In[13]:


Gus = True

if Gus:
    strings2 = {}
    for key in ahora_si.keys():
        _strings = []
        for _file in ahora_si[key]:
            with open(_file, 'r') as f:
              _strings.append(f.read())
        strings2.update({
            key: _strings
        })


# In[18]:


#print(strings[archivos[1]][1])


# In[19]:


#pool.close()
#pool.terminate()


# In[20]:


pool = mp.Pool()


# In[21]:


imagenes = pool.map(convert_from_path, caminos)


# In[22]:


archivos_en_imagenes = {
    archivo: imagen for archivo, imagen in zip(archivos, imagenes)
}


# In[23]:


# Muestra algún archivo :
#archivos_en_imagenes[archivos[3]][1]


# In[24]:


strings = images_to_strings(archivos_en_imagenes)


# In[13]:


# Send all of these files to texts/
save = False

if save:
    for nombre, hojas in strings.items():
        for i, hoja in enumerate(hojas):
            _file_name = os.path.join(path_textos, f"{nombre.replace('.pdf', '')}.{i}.txt")
            with open(_file_name, "w") as f:
                f.write(hoja)


# In[14]:


for lista in strings.values():
    for string in lista:
        print(regex.findall(r"\d{2}/\d{2}/\d{4}", string))


# In[15]:


_file = archivos[1]
print(_file)
print(len(strings[_file]))
print(strings[_file][2])


# In[17]:


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


# In[29]:


#print(foo)


# In[27]:


#print(tab_by_regex(strings[archivos[2]][0]))


# In[30]:


nombres


# In[28]:


archivos


# In[29]:


camino_resultados = os.path.abspath('segmented')
camino_resultados


# In[48]:


save_results(strings)


# In[38]:


os.mkdir('hue')


# In[34]:


for i, archivo in enumerate(archivos):
    for j, page in enumerate(strings[archivo]):
        with open(os.path.join(camino_resultados, f"{nombres[i]}.{j+1}.txt"), 'w') as f:
            f.write(tab_by_regex(page))


# In[19]:


newline = lambda x: f"{x}\n"
ntab = lambda n, txt: n*"\t" + txt


# In[27]:


_my_str = ''
for line in foo_lines:
    for i in regex.finditer(r"^([A-Z\s]|[A-Z]\.?)+?(?=(\..+))", line): # FIND lines starting with Caps 
        _my_str += newline(i.string)
        _my_str += newline(ntab(1, i.group()))
        for j in regex.finditer(r"(\d+\.\d+|\d+)", i.string): # find groups of numbers
            _my_str += newline(ntab(2, j.group()))
        for k in regex.finditer(r"(?<=(\d+\.\d+|\d+))\D[^\d]+?(?=\s)", i.string):
            _my_str += newline(ntab(3, k.group()))


# In[28]:


print(_my_str)


# In[31]:


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


# In[33]:


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


# In[34]:


dir(regex)
help(regex.purge)


# In[35]:


for line in foo_lines:
    for i in regex.findall(r"^[A-Z]{2,}", line):
        print(i)


# In[36]:


#dir(i)


# In[37]:


#i.expand()


# In[129]:


help(regex.compile)


# In[38]:


#regex.compile()


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




