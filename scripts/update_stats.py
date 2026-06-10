#!/usr/bin/env python3
"""
🍟 Lotto-Frite-Mayo — Mise à jour automatique des statistiques
Source : https://www.lotteryextreme.com/belgium/lotto-statistics(1)
"""

import requests
from bs4 import BeautifulSoup
import json, sys, time, random
from datetime import date

URL        = "https://www.lotteryextreme.com/belgium/lotto-statistics(1)"
STATS_FILE = "stats.json"

# User-Agents réalistes pour éviter le blocage
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "fr-BE,fr;q=0.9,en;q=0.8,nl;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

def load_existing():
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {"freq": {}, "date": ""}

def scrape(attempt=1):
    print(f"→ Tentative {attempt}/3 : {URL}")
    try:
        session = requests.Session()
        # Première requête sur la page principale (comme un vrai navigateur)
        session.get("https://www.lotteryextreme.com/", headers=get_headers(), timeout=20)
        time.sleep(random.uniform(1.5, 3.0))
        # Requête sur la page des stats
        resp = session.get(URL, headers=get_headers(), timeout=30)
        resp.raise_for_status()
        print(f"  HTTP {resp.status_code} — {len(resp.text)} caractères reçus")
    except Exception as e:
        print(f"  ERREUR fetch : {e}")
        return None

    soup = BeautifulSoup(resp.text, "lxml")
    freq = {}

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
            print(f"  ✓ {len(local)} numéros trouvés dans le tableau")
            freq = local
            break

    if not freq:
        print(f"  ⚠ Tableau de fréquences non trouvé (page peut-être bloquée)")
        # Debug : afficher les 500 premiers caractères du HTML reçu
        print(f"  Début du HTML : {resp.text[:300]}")
        return None

    # Compléter les manquants avec l'ancienne valeur
    existing = load_existing()
    missing = [i for i in range(1, 46) if str(i) not in freq]
    if missing:
        print(f"  ⚠ Manquants : {missing} → conserve ancienne valeur")
        for m in missing:
            if str(m) in existing.get("freq", {}):
                freq[str(m)] = existing["freq"][str(m)]

    return freq


def main():
    existing = load_existing()
    print(f"Données actuelles : {existing.get('date', 'inconnue')}")

    freq = None
    for attempt in range(1, 4):
        freq = scrape(attempt)
        if freq:
            break
        if attempt < 3:
            wait = attempt * 5
            print(f"  Pause {wait}s avant nouvelle tentative...")
            time.sleep(wait)

    if not freq or len(freq) < 40:
        print("❌ Scraping échoué après 3 tentatives — données inchangées.")
        # Exit 0 pour ne pas faire échouer le workflow
        sys.exit(0)

    if freq == existing.get("freq", {}):
        print("✓ Données identiques — aucune mise à jour nécessaire.")
        sys.exit(0)

    data = {
        "freq":   freq,
        "date":   date.today().isoformat(),
        "source": "lotteryextreme.com",
    }
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    top3 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:3]
    print(f"✅ stats.json mis à jour — {data['date']}")
    print(f"   Top 3 : " + ", ".join(f"N°{n} ({c}×)" for n, c in top3))


if __name__ == "__main__":
    main()
