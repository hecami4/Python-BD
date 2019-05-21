# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import os
import json
from collections import Counter

archivos_html = os.listdir('crawled/')


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    elif element == ' ' or element == '\n':
        return False

    return True


corpus = {}

output = ''

with open('output.json', 'r') as f:
    output = json.loads(json.dumps(json.loads(f.read())))


list_dict = []

for url_json in output:
    list_dict.append(json.loads(json.dumps(url_json)))

for archivo_html in archivos_html:
    soup = BeautifulSoup(open('crawled/' + archivo_html), "html.parser", from_encoding='utf-8')
    data = soup.findAll(text=True)

    palabras = filter(visible, data)

    archivo_txt = open('texto/' + str(archivo_html)[0:len(str(archivo_html)) - 5] + '.txt', 'w+')

    palabras_repetidas = []

    for palabra in palabras:
        archivo_txt.write(palabra.encode('utf-8') + '\n')
        palabras_particionada = palabra.split(' ')

        for palabra_particionada in palabras_particionada:
            palabra_particionada = str(palabra_particionada.encode('utf-8')).lower()
            if palabra_particionada == '' or palabra_particionada == ' ' or len(palabra_particionada) < 4:
                continue

            palabras_repetidas.append(palabra_particionada)

            if palabra_particionada in corpus:
                corpus[palabra_particionada].append(archivo_html)
            else:
                corpus[palabra_particionada] = []
                corpus[palabra_particionada].append(archivo_html)

    for dicty in list_dict:
        if str(archivo_html[-5]) in str(dicty.keys()[0]):
            dicty.values()[0]["palabras"] = {}

            for ocurrencia in Counter(palabras_repetidas).items():
                dicty.values()[0]["palabras"][str(ocurrencia[0])] = ocurrencia[1]


with open('corpus.json', 'w') as fp:
    json.dump(corpus, fp)

with open('output_indexado.json', 'w') as fp:
    fp.write(json.dumps(list_dict))

