# 🍟 Lotto-Frite-Mayo

> *"Les meilleures combinaisons… toujours meilleures avec de la mayo."*

Générateur de combinaisons Lotto belge basé sur l'analyse statistique des tirages depuis 1978. 100% belge, 100% frites.

---

## ✨ Fonctionnalités

- **5 stratégies** : Les Chauds, L'Équilibre, Paires d'Or, Anti-Splitting, Mixte Optimisé
- **2 modes** : combinaison fixe ou variation aléatoire dans le pool de la stratégie
- **Sélecteur de date** pour le tirage mercredi ou samedi
- **Réactualisation live** des statistiques via l'API Anthropic (clé requise)
- **Persistance** : les stats fraîches sont mémorisées dans ton navigateur

---

## 🚀 Mise en ligne sur GitHub Pages (5 minutes)

### Étape 1 — Créer le dépôt
1. Va sur [github.com](https://github.com) et connecte-toi
2. Clique **"New repository"** → nom : `lotto-frite-mayo`
3. Laisse-le en **Public** → **"Create repository"**

### Étape 2 — Uploader les fichiers
1. Dans le dépôt vide, clique **"uploading an existing file"**
2. Glisse-dépose `index.html` et `README.md`
3. Clique **"Commit changes"**

### Étape 3 — Activer GitHub Pages
1. **Settings** → **Pages** (menu gauche)
2. Source : **Deploy from a branch** → Branch : **main** → Folder : **/ (root)** → **Save**

### Étape 4 — C'est en ligne ! 🎉
Attends ~1 minute puis visite :
```
https://TON-USERNAME.github.io/lotto-frite-mayo/
```

---

## 🔑 Clé API Anthropic (optionnelle)

Le bouton **⟳ Réactualiser** utilise l'API Anthropic pour récupérer les vraies statistiques en temps réel.

**Sans clé** → l'app fonctionne parfaitement avec les stats intégrées (mai 2026).  
**Avec clé** → stats mises à jour en direct depuis LotteryExtreme.com.

1. Crée un compte sur [console.anthropic.com](https://console.anthropic.com)
2. Génère une clé API dans "API Keys"
3. Dans l'app : clique ⚙️ et colle ta clé

> ⚠️ Ne partage jamais ta clé publiquement. Elle est sauvegardée uniquement dans ton navigateur.

---

## 📊 Les 5 stratégies

| Stratégie | Logique |
|-----------|---------|
| 🔥 **Les Chauds** | Top 6 numéros les plus tirés depuis 1978 |
| ⚖️ **L'Équilibre** | 3 chauds + 3 numéros très en retard |
| 💎 **Paires d'Or** | Basé sur le triplet 12-28-36 (sorti 20× ensemble) |
| 🧠 **Anti-Splitting** | Numéros >31 pour réduire le partage du jackpot |
| 🎯 **Mixte Optimisé** | Synthèse multi-critères équilibrée |

---

## 📂 Structure

```
lotto-frite-mayo/
├── index.html   ← application complète (fichier unique, zéro dépendance)
└── README.md    ← ce fichier
```

Aucun `npm install`, aucun build. Ouvre `index.html` dans ton navigateur, et c'est parti.

---

## 🧑‍💻 À propos

- **Développeur** : borsup 🇧🇪  
- **Version** : 1.0  
- **Date** : Juin 2026  
- **Données** : [LotteryExtreme.com](https://www.lotteryextreme.com/belgium/lotto-statistics) · ~5 000 tirages · 1978–2026

---

⚠️ Le Lotto est un jeu de hasard. Joue responsable. **0800 35 777** (gratuit, anonyme)
