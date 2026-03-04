# 🌍 Flag Quiz Bot — Discord

Bot Discord de quiz des drapeaux avec système de score et classement.  
Affiche un drapeau aléatoire sous forme d'emoji et propose 4 choix dont un seul est correct.

---

## 🎮 Commandes

| Commande | Description |
|---|---|
| `/drapeau` | Affiche un drapeau + 4 boutons (1 bonne réponse, 3 leurres) |
| `/score` | Affiche ton score personnel (message privé) |
| `/classement` | Affiche le top 10 des joueurs du serveur |

---

## 📁 Structure du projet

```
flag-quiz-bot/
├── bot.py             # Code principal du bot
├── requirements.txt   # Dépendances Python
├── Procfile           # Instruction de démarrage pour Railway
├── .env.example       # Template de configuration locale
└── README.md          # Ce fichier
```

---

## 🚀 Installation locale

### Prérequis

- Python 3.10 ou supérieur
- Un token de bot Discord (voir ci-dessous)

### 1. Cloner le dépôt

```bash
git clone https://github.com/TON_USERNAME/flag-quiz-bot.git
cd flag-quiz-bot
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer le token

Copie `.env.example` en `.env` et remplace la valeur :

```bash
cp .env.example .env
```

Contenu du `.env` :

```
DISCORD_TOKEN=ton_token_ici
```

### 4. Lancer le bot

```bash
python bot.py
```

---

## ☁️ Déploiement sur Railway

### 1. Préparer le repo GitHub

Assure-toi que ces fichiers sont présents à la racine :

- `bot.py`
- `requirements.txt`
- `Procfile` (contenu : `worker: python bot.py`)

> ⚠️ Utilise `worker` et non `web` — un bot Discord n'expose pas de port HTTP.

### 2. Créer le projet sur Railway

1. Va sur [railway.app](https://railway.app)
2. **New Project → Deploy from GitHub repo**
3. Sélectionne ton dépôt

### 3. Ajouter la variable d'environnement

Dans ton service Railway → onglet **Variables** :

| Nom | Valeur |
|---|---|
| `DISCORD_TOKEN` | `ton_token_discord` |

Railway installe automatiquement les dépendances via `requirements.txt`.

---

## 🔑 Obtenir un token Discord

1. Connecte-toi sur [discord.com/developers/applications](https://discord.com/developers/applications)
2. **New Application** → donne un nom à ton bot
3. Onglet **Bot** → **Reset Token** → copie le token
4. Active l'option **Message Content Intent** si besoin

### Inviter le bot sur ton serveur

Dans **OAuth2 → URL Generator** :

- **Scopes** : `bot`, `applications.commands`
- **Permissions** : `Send Messages`, `Embed Links`

Copie l'URL générée et ouvre-la dans ton navigateur.

---

## ➕ Ajouter des pays

Dans `bot.py`, le dictionnaire `COUNTRIES` contient toutes les paires `"Nom du pays": "🏳️"`.  
Ajoute simplement une nouvelle ligne pour enrichir le quiz :

```python
COUNTRIES = {
    "France": "🇫🇷",
    "Nouveau pays": "🏳️",  # ← ajoute ici
    ...
}
```

---

## ⚠️ Limitations connues

- Les scores sont stockés **en mémoire** et sont réinitialisés à chaque redémarrage du bot.
- Pour une persistance des scores, il faut intégrer une base de données (SQLite, PostgreSQL, etc.).

---

## 📄 Licence

Projet libre — utilise-le et modifie-le comme tu le souhaites.
