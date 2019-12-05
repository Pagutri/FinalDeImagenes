#!/usr/bin/env python
# coding: utf-8

# In[29]:


import os
import regex
import glob
import multiprocessing as mp
import importlib
import pprint

from typing import Tuple, Callable, Any, NoReturn, List, Dict, Optional

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


# In[5]:


import timing
importlib.reload(timing)
import timing


# In[19]:


# Instantiate a multiprocess pool.
pool = mp.Pool()


# In[50]:


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
def dict_from_regex(x: str) -> str:
    """
    """
    
    _x_lines: List[str] = x.split('\n')
    
    _dict2 = {}
    for line in _x_lines:
        for i in regex.finditer(r"^([A-Z\s]|[A-Z]\.?)+?(?=(\..+))", line): 
            i.group()
            _valores = []
            _unidades = []
            for j in regex.finditer(r"(\d+\.\d+|\d+)", i.string): # find groups of numbers
                _valores.append(j.group())
            for k in regex.finditer(r"(?<=(\d+\.\d+|\d+))\D[^\d]+?(?=\s)", i.string):
                _unidades.append(k.group())
            if len(_valores) < 4 and len(_unidades) < 4:
                _dict2.update({
                    i.group(): {
                        "values": _valores,
                        "units": _unidades
                    }
                })
    
    return _dict2
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

@timing.time_log()
def extract_date(x: Dict[str, List[str]], exclude_date: Optional[str] = None):
    dates = {}
    for nombre, lista in x.items():
        _tmp_list = []
        for string in lista:
            _tmp_list += list(set(
                regex.findall(r"(\d{2}\D[A-Z]{3}\D\d{4}|\d{2}\D\d{2}\D\d{4})", string)
            ))
        dates.update({
            nombre: list(set(_tmp_list))
        })

    if exclude_date is not None:
        for nombre, lista in dates.items():
            dates[nombre] = lfilter(lambda x: x if x != exclude_date else False, lista)
    
    return dates
##


# In[51]:


lol = dict_from_regex(strings[archivos[1]][1])
lol


# In[ ]:





# In[33]:


newline = lambda x: f"{x}\n"
ntab = lambda n, txt: n*"\t" + txt


# In[7]:


path = os.path.abspath('analisis_clinicos/')
path


# In[8]:


path_textos = os.path.abspath('textos')
path_textos


# In[9]:


caminos_textos = glob.glob(f"{path_textos}/*.txt")
caminos_textos.sort()
#caminos_textos


# In[10]:


caminos = glob.glob(f"{path}/*.pdf")
#caminos


# In[11]:


archivos = [ os.path.split(camino)[1] for camino in caminos]
archivos


# In[12]:


nombres = [ archivo.replace('.pdf', '') for archivo in archivos ]
nombres


# In[13]:


ahora_si = { 
    archivo: glob.glob(os.path.join(path_textos ,f"{nombre}.?.txt")) 
    for archivo, nombre in zip(archivos, nombres)
}


# In[14]:


[ ahora_si[key].sort() for key in ahora_si.keys() ]
#ahora_si


# In[15]:


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


# In[16]:


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


# In[34]:


# Obtain text from the PDFs, directly (this takes about a minute) : 
from_scratch = False

if from_scratch:
    imagenes = pool.map(convert_from_path, caminos)
    archivos_en_imagenes = {
        archivo: imagen for archivo, imagen in zip(archivos, imagenes)
    }
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


# In[22]:


for lista in strings.values():
    for string in lista:
        print(regex.findall(r"\d{2}/\d{2}/\d{4}", string))


# In[23]:


dates = {}
for nombre, lista in strings.items():
    _tmp_list = []
    for string in lista:
        _tmp_val = set(regex.findall(r"(\d{2}\D[A-Z]{3}\D\d{4}|\d{2}\D\d{2}\D\d{4})", string))
        if len(_tmp_list) == 0:
            _tmp_list.append(_tmp_val)
        else:
            if _tmp_val not in _tmp_list:
                _tmp_list.append(_tmp_val)
    dates.update({
        nombre: _tmp_list
    })
pprint.pprint(dates)


# In[26]:


dates = {}
for nombre, lista in strings.items():
    _tmp_list = []
    for string in lista:
        _tmp_list += list(set(
            regex.findall(r"(\d{2}\D[A-Z]{3}\D\d{4}|\d{2}\D\d{2}\D\d{4})", string)
        ))
    dates.update({
        nombre: list(set(_tmp_list))
    })

for nombre, lista in dates.items():
    dates[nombre] = lfilter(lambda x: x if x != someval else False, lista)
    

pprint.pprint(dates)


# In[37]:


print(tab_by_regex(strings[archivos[1]][0]))


# In[3]:


s = set([1, 2, 3, 3])


# In[86]:


s.discard(1)
len(s)


# In[85]:


len(s.difference(s))


# In[83]:


dif.


# In[52]:


nombres


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


#pool.close()
#pool.terminate()

