"""
   projekt_3.py: Třetí projekt do Engeto Online Python Akademie

   author: Šárka Praxová
   email: sarka.praxova@seznam.cz
   """
import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin
import re
import os

def je_spravny_odkaz(odkaz):
    return re.match(r"^https://www\.volby\.cz/pls/ps2017nss/ps32.*", odkaz)

def ziskej_html(url):
    odpoved = requests.get(url)
    if odpoved.status_code == 200:
        return BeautifulSoup(odpoved.text, "html.parser")
    else:
        print(f"Chyba při načítání stránky: {url}")
        return None

def ziskej_odkazy_na_obce(soup, zakladni_url):
    odkazy = []
    for a in soup.select("td.cislo a"):
        cast_url = a["href"]
        cele_url = urljoin(zakladni_url, cast_url)
        kod_obce = a.text.strip()
        odkazy.append((kod_obce, cele_url))
    return odkazy

def zpracuj_obec(kod_obce, url):
    soup = ziskej_html(url)
    if not soup:
        return None

    # Získání názvu obce z nadpisu
    nazev_obce = ""
    for nadpis in soup.find_all("h3"):
        if "Obec:" in nadpis.text:
            nazev_obce = nadpis.text.split("Obec:")[1].strip()
            break

    try:
        voliči = soup.find("td", {"headers": "sa2"}).text.strip()
        obalky = soup.find("td", {"headers": "sa3"}).text.strip()
        platne = soup.find("td", {"headers": "sa6"}).text.strip()
    except AttributeError:
        print(f"Chyba při čtení dat obce {kod_obce}")
        return None

    vysledky = {
        "kód obce": kod_obce,
        "název obce": nazev_obce,
        "voliči v seznamu": voliči,
        "vydané obálky": obalky,
        "platné hlasy": platne
    }

    strany = soup.select("td.overflow_name")
    hlasy = soup.select("td.overflow_name + td")

    for strana, hlas in zip(strany, hlasy):
        vysledky[strana.text.strip()] = hlas.text.strip()

    return vysledky

def hlavni(url, vystupni_soubor):
    print(f"Stahuji data z vybraného URL: {url}")

    base_url = "https://www.volby.cz/pls/ps2017nss/"
    hlavni_soup = ziskej_html(url)
    if not hlavni_soup:
        print("Nepodařilo se načíst hlavní stránku.")
        return

    obce_odkazy = ziskej_odkazy_na_obce(hlavni_soup, base_url)

    vysledky = []
    vsechny_strany = set()

    for kod_obce, obec_url in obce_odkazy:
        print(f"Zpracovávám obec {kod_obce}...")
        data = zpracuj_obec(kod_obce, obec_url)
        if data:
            vysledky.append(data)
            vsechny_strany.update(data.keys())

    zakladni_sloupce = ["kód obce", "název obce", "voliči v seznamu", "vydané obálky", "platné hlasy"]
    strany_sloupce = sorted(vsechny_strany - set(zakladni_sloupce))
    vsechny_sloupce = zakladni_sloupce + strany_sloupce

    print(f"Ukládám do souboru: {vystupni_soubor}")
    with open(vystupni_soubor, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=vsechny_sloupce)
        writer.writeheader()
        for radek in vysledky:
            writer.writerow(radek)

    print(f"Ukončuji skript: {os.path.basename(__file__)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Chyba: Zadejte 2 argumenty – odkaz a jméno výstupního souboru.")
        print("Příklad použití:")
        print("   python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101 vysledky_benesov.csv")
        sys.exit(1)

    odkaz = sys.argv[1]
    vystupni_soubor = sys.argv[2]

    if not je_spravny_odkaz(odkaz):
        print("Chyba: První argument musí být platný odkaz na stránku volby.cz (např. kraj).")
        sys.exit(1)

    hlavni(odkaz, vystupni_soubor)

