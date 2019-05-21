# -*- coding: utf-8 -*-

import json
from bs4 import BeautifulSoup
from w3lib.html import remove_tags

output = ''

def calculo_ranking(output):
    list_dict = []

    with open('output_indexado.json', 'r') as f:
        output = json.loads(json.dumps(json.loads(f.read())))

        for url_json in output:
            list_dict.append(json.loads(json.dumps(url_json)))

        for dicty in list_dict:
            dicty.values()[0]["ranking"] = 0.156496876

    return list_dict


list_dict = calculo_ranking(output)


def realizar_busqueda(clave, list_dict):
    palabras_clave = clave.split()

    relevancia = {}

    for dicty in list_dict:
        palabras_dict = dicty.values()[0]["palabras"]

        contador_ocurrencias = 0

        for k, v in palabras_dict.items():
            if k in palabras_clave:
                contador_ocurrencias += v

        relevancia[dicty.keys()[0]] = contador_ocurrencias

    print('Resultados de la busqueda: ')
    contador_resultado = 0

    for key in sorted(relevancia.iterkeys()):
        print('Resultado: ' + str(contador_resultado))
        print(" ")
        for dicty in list_dict:
            if dicty.keys()[0] == key:
                print("Titulo pagina: " + u''.join(dicty.values()[0]["titulo"]).encode('utf-8'))

        print(" ")
        soup = BeautifulSoup(open('crawled/' + str(key).split("/")[-1] + ".html"), "html.parser", from_encoding='utf-8')
        print(str(soup('p')[0]))

        print(' ')

        print("%s: %s" % ("URL: ", key))

        print(" ")
        print("Relevancia busqueda: %s" % (str(len(relevancia) - contador_resultado)))

        contador_resultado = contador_resultado + 1

        print(" ")
        print("Ranking Pagina: " + str(dicty.values()[0]["ranking"]))

        print(" ")
        print(" ")


clave = str(raw_input("Ingresa las palabras que quieres buscar: "))

if len(clave) > 2:
    realizar_busqueda(clave, list_dict)
else:
    print("Debe digitar al menos 3 caracteres")
