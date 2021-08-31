# Vote scraper projekt
## Popis projektu
Tento projekt se zabývá scrapováním výsledků voleb do Poslanecké sněmovny Parlamentu České republiky z roku 2017. Na zdrojový web se můžete podívat [zde.](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

## Instalace knihoven
Pro spuštění projektu budete potřebovat několik knihoven, jejichž seznam naleznete v přeloženém souboru `requirements.txt`.
Pokud máte nainstalovaný manažer stačí zadat do konzole následující příkaz, pomocí kterého všechny potřebné knihovny nainstalujete.

```
pip install -r requirements.txt
```
## Spuštění projektu
Pro spuštění samotného projektu budete muset do příkazového řádku zapsat následující:
```
python volby.py "link" "nazev_souboru"
```
Do příkazového řádku tedy zapíšete název spouštěného kódu (v našem případě volby.py), následně link na územní celek, jehož výsledky chcete scrapovat a nakonec název souboru, do kterého chcete výsledky uložit.

## Ukázka běhu projektu
Nyní si ukážeme, jak samotný projekt funguje. V našem případě budeme scrapovat výsledky z volebního okrsku Jeseník. Do příkazového řádku tedy vložíme následující:
```
volby.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7101" "vysledky_jesenik.csv"
```
Po spuštění uvidíme postupně následující hlášky, odpovídající správnému běhu programu.

```
Stahuji data z vybraného URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7101
Ukládám do souboru: vysledky_jesenik.csv
Ukončuji volby.py

```
Výsledky jsou zapsány do souboru výsledky_jesenik.csv. Příklad výstupu můžete vidět níže. 
```
code,location,registred,envelopes,valid,Občanská demokratická strana, ...
523917,Bělá pod Pradědem,1 546,945,938,77,1,0,47,2,53,70,8,12,10, 0, ...
524891,Bernartice,703,344,343,24,0,0,25,1,6,38,1,1,1,0,0,15,0,5,149, ...
```
V případě, že se program pokusíme zkusit bez patříčných inputů, obdržíme následující hlášku.
```
Zadali jste nesprávné vstupní argumenty.
Pro správnou funkčnost programu zadejte nejdříve odkaz,
ze kterého chcete scrapovat, a následně soubor, do kterého chcete ukládat.
```