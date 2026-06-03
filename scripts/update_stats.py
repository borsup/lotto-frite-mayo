#!/usr/bin/env python3
"""
🍟 Lotto-Frite-Mayo — Mise à jour automatique des statistiques
Source : https://www.lotteryextreme.com/belgium/lotto-statistics(1)
Lancé chaque lundi par GitHub Actions (gratuit).
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import date

URL        = "https://www.lotteryextreme.com/belgium/lotto-statistics(1)"
STATS_FILE = "stats.json"
HEADERS    = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "fr-BE,fr;q=0.9,en;q=0.8",
    "Cache-Control":   "no-cache",
}


def load_existing():
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"freq": {}, "date": ""}


def scrape():
    print(f"→ Fetching: {URL}")
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        print(f"  ERREUR fetch : {e}")
        return None

    soup  = BeautifulSoup(resp.text, "html.parser")
    freq  = {}

    # Parcourt toutes les tables pour trouver la table des fréquences (numéros 1-45)
    for table in soup.find_all("table"):
        local = {}
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 2:
                continue
            texts = [c.get_text(strip=True).replace(",", "").replace(".", "") for c in cells]
            for i in range(len(texts) - 1):
                try:
                    num   = int(texts[i])
                    count = int(texts[i + 1])
                    if 1 <= num <= 45 and 50 <= count <= 2000:
                        local[str(num)] = count
                except ValueError:
                    continue
        if len(local) >= 40:
            print(f"  ✓ {len(local)} numéros trouvés")
            freq = local
            break

    if not freq:
        print("  ERREUR : table de fréquences introuvable")
        return None

    # Complète les éventuels manquants avec l'ancienne valeur
    existing = load_existing()
    missing  = [i for i in range(1, 46) if str(i) not in freq]
    if missing:
        print(f"  ⚠ Numéros manquants : {missing} → conserve l'ancienne valeur")
        for m in missing:
            if str(m) in existing.get("freq", {}):
                freq[str(m)] = existing["freq"][str(m)]

    return freq


def main():
    existing = load_existing()
    freq     = scrape()

    if not freq or len(freq) < 40:
        print("Scraping échoué — données inchangées.")
        sys.exit(0)

    if freq == existing.get("freq", {}):
        print("Données identiques — aucune mise à jour nécessaire.")
        sys.exit(0)

    data = {
        "freq":   freq,
        "date":   date.today().isoformat(),
        "source": "lotteryextreme.com",
    }
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    top3 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"✅ stats.json mis à jour ({len(freq)} numéros) — {data['date']}")
    print(f"   Top 3 : " + ", ".join(f"N°{n} ({c}×)" for n, c in top3))


if __name__ == "__main__":
    main()

