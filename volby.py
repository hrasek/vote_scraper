import re
import sys

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
import csv


# Program scrapuje výsledky voleb do Poslanecké sněmovny Parlamentu České republiky z roku 2017.\ Vyscrapuje vždy výsledky z jednoho územního celku a vrací tabulku z výsledky v jednotlivých obcích.

def tabulka_uzemni_celek(odkaz): # Funkce bere jako vstup odkaz na stránku s územním celkem a jako výstup dává tabulku s jednotlivými obcemi v tomto územním celku.
    tabulky = pd.read_html(odkaz, encoding='utf-8')
    radky = []
    for tabulka in tabulky:
        for radek in filter(lambda x: x != ['-', '-', '-'], tabulka.values.tolist()): # Filtrování prázdných řádků.
            radky.append(radek)
    return radky


def stahni_odkazy(odkaz): # Funkce bere jako vstup odkaz na stránku s územním celkem a jako výstup dává odkazy na výsledky voleb v jednotlivých obcích.
    r = requests.get(odkaz)
    soup = BS(r.text, "html.parser")
    a = soup.find_all('a')
    links = []
    for acka in a:
        links.append('https://volby.cz/pls/ps2017nss/' + acka.get('href')) # Dává odkazu odpovídající podobu. Následuje filtrování nepotřebných odkazů.
    links = links[5:-2]
    if len(links) % 2 == 1: # tzv. varianta Brno. Pro okres Brno-město má stránka trochu jinou strukturu, než pro ostatní okresy.
        links = links[::3]
    else:
        links = links[::2]
    return links


def tabulka_obce(link): # Funkce bere jako vstup odkaz na stránku s výsledky v dané obci a vrací tabulky s výsledky v nich.
    tabulky = pd.read_html(link, encoding='utf-8')
    info = tabulky[0].values.tolist()
    info = [info[0][3], info[0][4], info[0][7]]
    tabulka = tabulky[1].values.tolist() + tabulky[2].values.tolist()
    strany = []
    vysledky = []
    for radek in tabulka:
        if radek != ['-', '-', '-', '-', '-']:
            strany.append(radek[1])
            vysledky.append(radek[2])
    return info, vysledky, strany


def zapis_do_slovniku(slovnik, strany, vysledky, poradi_obce): # Funkce bere jako vstup slovnik, do kterého mají být zapsaný výsledky voleb, dále seznam stran a jejich výsledky a nakonec pořadí obce v daném seznamu obcí. Jako výstup dává slovník se zahrnutými výsledky.
    for index, strana in enumerate(strany):
        pocet_hlasu = int(re.sub('\xa0', '', str(vysledky[index])))
        if strana in slovnik.keys():
            slovnik[strana].append(pocet_hlasu)
        elif slovnik:
            listofzeros = [0] * (poradi_obce - 1)
            slovnik.update({strana: listofzeros + [pocet_hlasu]})
        else:
            slovnik.update({strana: [pocet_hlasu]})

    return slovnik


def write_to_file(name, radky, nadpis): # Funkce bere jako vstup název souboru, do kterého má zapsat, poté data a také jejich nadpis. To jsou zapsány do souboru s odpovídajícím názvem.
    with open(name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(nadpis)
        writer.writerows(radky)

try:
    odkaz = sys.argv[1]
    name = sys.argv[2]
except IndexError: # Vypořádání se se špatným voláním programu.
    sys.exit('Zadali jste nesprávné vstupní argumenty.\nPro správnou funkčnost programu zadejte argumenty nejdříve odkaz,\nze kterého chcete scrapovat, a následně soubor, do kterého chcete ukládat. ')

nadpis = ['code', 'location', 'registred', 'envelopes', 'valid']
print('Stahuji data z vybraného URL: {}'.format(odkaz))
info_obce = tabulka_uzemni_celek(odkaz)

links = stahni_odkazy(odkaz)
strany_slovnik = dict()
radky = []

for index, link in enumerate(links):
    info, vysledky, strany_list = tabulka_obce(link)

    strany_slovnik = zapis_do_slovniku(strany_slovnik, strany_list, vysledky, index + 1)
    hlasy = [item[index] for item in list(strany_slovnik.values())]
    radky.append(info_obce[index][0:-1] + info + hlasy)

nadpis.extend(list(strany_slovnik.keys()))
print('Ukládám do souboru: {}'.format(name))
write_to_file(name, radky, nadpis)
print('Ukončuji volby.py')
