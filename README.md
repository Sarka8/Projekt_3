# Engeto-pa-3-projekt
Třetí projekt v Python akademii od Engeta. 

## Popis projektu

Tento projekt slouží k extrahování výsledků parlamentních voleb v r. 2017. Odkaz k prohlédnutí najdete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace knihoven

Knihovny, které jsou použity v kódu, jsou vložené v souboru * `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následně:

```bash
$ pip3 --version                        # ověřím verzi manageru 
$ pip3 install -r requirements.txt      # nainstalujeme knihovny
```
## Spuštění projektu

Pro spuštění souboru main.py v rámci příkazového řádku jsou požadovány dva argumenty:

```bash
python main.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Následně se vám stáhnou výsledky jako soubor s příponou .csv.

## Ukázka projektu

Výsledky hlasování pro okres Benešov:

1. argument: * `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101`
2. argument: * `vysledky_benesov.csv`

Spuštění programu:

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv
```
Průběh stahování:

```bash
Stahuji data z vybraného URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
Zpracovávám obec 529303...
Zpracovávám obec 532568...
Zpracovávám obec 530743...
Zpracovávám obec 532380...
Ukládám do souboru: vysledky_benesov.csv
Ukončuji skript: main.py
```
Částečný výstup:

```bash
kód obce,název obce,voliči v seznamu,vydané obálky,platné hlasy,...
529303,Benešov,13 104,8 485,8 437,2 577,6,2,3,16,597,314,11,1 052,58,35,3,6,17,21,802,10,112,109,682,414,3,948,624,5,10
532568,Bernartice,191,148,148,39,0,0,0,0,7,37,0,4,3,4,0,0,0,0,6,0,0,1,20,3,0,7,17,0,0
```

Soubor CSV obsahuje:

* `kód obce`
* `název obce`
* `voliči v seznamu`
* `vydané obálky`
* `platné hlasy`
* `sloupce pro všechny kandidující strany (s počtem hlasů)`
