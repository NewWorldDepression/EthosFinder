# 🌐 DNSDumpster Integration - ETHOS FINDER v2.1

## 📖 Vue d'ensemble

Cette mise à jour ajoute la **reconnaissance de domaines** à ETHOS FINDER via l'intégration DNSDumpster. Vous pouvez maintenant effectuer des recherches DNS complètes, découvrir des sous-domaines et cartographier l'infrastructure réseau d'un domaine.

---

## ✨ Nouvelles fonctionnalités

### 🔍 Recherche de domaines
- Enregistrements DNS (A, MX, TXT, NS, SOA, etc.)
- Découverte de sous-domaines
- Résolution d'adresses IP
- Cartographie de l'infrastructure

### 🔐 Sécurité renforcée
- Stockage chiffré des clés API
- Support des variables d'environnement
- Mode fallback sans API
- Validation stricte des entrées

### 🛠️ Outils complémentaires
- Énumération locale de sous-domaines
- Lookup DNS public (sans API)
- Export des résultats en JSON
- Gestion des erreurs robuste

---

## 🚀 Installation rapide

### 1. Mettre à jour le code

```bash
# Si vous utilisez Git
git pull origin main

# Ou téléchargez les nouveaux fichiers
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer votre clé API (optionnel)

**Option A - Via l'interface:**
```bash
python ethos.py
# Menu: 7 (Settings) → 4 (Add DNSDumpster API Key)
```

**Option B - Variable d'environnement (recommandé):**
```bash
# Windows
set ETHOS_DNSDUMPSTER_KEY=votre_clé_api

# Linux/Mac
export ETHOS_DNSDUMPSTER_KEY=votre_clé_api
```

**Option C - Fichier de configuration:**
```json
{
  "dnsdumpster_api_key": "votre_clé_api",
  "rapidapi_key": "",
  "rapidapi_hosts": {}
}
```

### 4. Lancer une recherche

```bash
python ethos.py
# Menu: 4 (Find by DOMAIN)
# Entrez: example.com
```

---

## 📋 Utilisation

### Exemple basique

```bash
$ python ethos.py

╔══════════════════════════════════════════════════╗
║         ETHOS FINDER v2.1 - OSINT Tool          ║
╚══════════════════════════════════════════════════╝

1) 📧 Find by EMAIL
2) 📱 Find by PHONE NUMBER
3) 👤 Find by USERNAME
4) 🌐 Find by DOMAIN (DNSDumpster)    ← NOUVEAU !
5) (SOON) Find by NAME/SURNAME
6) (SOON) Find by PUBLIC IP
7) ⚙️  SETTINGS
8) 🔄 RESET CONFIG
9) 🚪 EXIT

Your choice: 4

Enter domain (e.g., example.com): google.com

[*] Starting domain reconnaissance...
[+] DNSDumpster API key found - using API search
[+] API search completed successfully

RESULTS:
{
  "domain": "google.com",
  "dns_records": {
    "A": ["142.250.185.46", "142.250.185.78"],
    "MX": ["smtp.google.com"],
    "NS": ["ns1.google.com", "ns2.google.com"],
    "TXT": ["v=spf1 include:_spf.google.com ~all"]
  },
  "subdomains": [
    "www.google.com",
    "mail.google.com",
    "drive.google.com",
    "docs.google.com"
  ],
  "method": "api"
}
```

### Mode sans API

Si vous n'avez pas de clé API, ETHOS utilise un lookup DNS basique:

```bash
[i] No DNSDumpster API key configured
[i] Using basic public DNS lookup (limited results)
[i] Configure API key in Settings for full results

RESULTS:
{
  "domain": "example.com",
  "ip_addresses": ["93.184.216.34"],
  "note": "Public lookup - limited information",
  "method": "public"
}

Would you like to enumerate subdomains? (y/N): y

[i] Enumerating subdomains for example.com...
[i] Testing 40 common subdomain names...
  [+] Found: www.example.com
  [+] Found: mail.example.com
[+] Found 2 active subdomains
```

---

## 📁 Nouveaux fichiers

```
EthosFinder/
├── tools/
│   └── dnsdumpster_search.py    ← Module principal DNSDumpster
├── ethos.py                     ← Mis à jour avec option 4
├── secure_config.py             ← Support DNSDumpster key
├── demo_dnsdumpster.py          ← Script de démonstration
├── DNSDUMPSTER_GUIDE.md         ← Guide complet
├── CHANGELOG_DNSDUMPSTER.md     ← Journal des changements
└── README_DNSDUMPSTER.md        ← Ce fichier
```

---

## 🎯 Cas d'usage

### 🐛 Bug Bounty
```bash
# 1. Découvrir l'infrastructure
python ethos.py → Option 4 → target.com

# 2. Énumérer les sous-domaines
# Répondre 'y' à l'invite

# 3. Rechercher des points d'entrée non sécurisés
# Analyser les résultats JSON
```

### 🔒 Audit de sécurité
```bash
# Vérifier la surface d'attaque de votre domaine
python ethos.py → Option 4 → votredomaine.com

# Identifier les actifs exposés
# Vérifier les enregistrements DNS
# Détecter les sous-domaines non documentés
```

### 🎓 Apprentissage OSINT
```bash
# Exécuter le script de démonstration
python demo_dnsdumpster.py

# Choisir mode interactif
# Tester différents domaines
# Observer les résultats
```

---

## ⚙️ Configuration avancée

### Menu Settings (Option 7)

```
╔══════════════════════════════════════════════════╗
║                 SETTINGS MENU                    ║
╚══════════════════════════════════════════════════╝

1) 🔑 ADD RapidAPI Key
2) 🗑️  REMOVE RapidAPI Key
3) 📋 LIST Configured APIs
4) 🔐 ADD DNSDumpster API Key      ← NOUVEAU !
5) 🗑️  REMOVE DNSDumpster API Key   ← NOUVEAU !
6) 📊 VIEW All Configuration       ← Mis à jour
7) ⬅️  BACK to Main Menu
```

### Variables d'environnement

```bash
# Configuration sécurisée (recommandé en production)
export ETHOS_RAPIDAPI_KEY="your_rapidapi_key"
export ETHOS_DNSDUMPSTER_KEY="your_dnsdumpster_key"

# Lancer ETHOS
python ethos.py
```

### Chiffrement des clés

```bash
# Installer cryptography pour le chiffrement
pip install cryptography

# Les clés seront automatiquement chiffrées dans config.json
# La clé de chiffrement est stockée dans .ethos_key (fichier caché)
```

---

## 🧪 Tests et démonstration

### Script de démonstration

```bash
# Lancer toutes les démos
python demo_dnsdumpster.py
# Choisir option 1

# Mode interactif
python demo_dnsdumpster.py
# Choisir option 2

# Voir la configuration
python demo_dnsdumpster.py
# Choisir option 3
```

### Tests manuels

```bash
# Test 1: Domaine valide avec API
python ethos.py → 4 → google.com

# Test 2: Sans API (mode public)
python ethos.py → 4 → example.com

# Test 3: Avec énumération
python ethos.py → 4 → microsoft.com → y

# Test 4: Domaine invalide
python ethos.py → 4 → invalid_domain
```

---

## 🔒 Sécurité et confidentialité

### ✅ Bonnes pratiques

1. **Utilisez les variables d'environnement**
   ```bash
   export ETHOS_DNSDUMPSTER_KEY="your_key"
   ```

2. **Activez le chiffrement**
   ```bash
   pip install cryptography
   ```

3. **Ne commitez jamais config.json**
   ```bash
   # Déjà dans .gitignore
   config.json
   .ethos_key
   ```

4. **Renouvelez vos clés régulièrement**
   ```bash
   python ethos.py → 7 → 5 (Remove) → 4 (Add new)
   ```

### ⚖️ Usage légal

**✓ Autorisé:**
- Vos propres domaines
- Avec autorisation écrite
- Bug bounty programs
- Recherche académique

**✗ Interdit:**
- Scan non autorisé
- Exploitation de vulnérabilités
- Violation de confidentialité
- Usage malveillant

---

## 🐛 Résolution de problèmes

### Problème: "Invalid domain format"

**Solution:**
```bash
# ✓ Formats valides
example.com
subdomain.example.com
test.co.uk

# ✗ Formats invalides
http://example.com     # Pas d'URL
example                # Pas de TLD
192.168.1.1           # Pas d'IP
```

### Problème: "No module named 'dnsdumpster_search'"

**Solution:**
```bash
# Vérifier la structure
ls tools/dnsdumpster_search.py

# Réinstaller si nécessaire
git pull origin main
```

### Problème: "Authentication failed"

**Solution:**
```bash
# Vérifier la clé API
python ethos.py → 7 → 6

# Régénérer une nouvelle clé sur DNSDumpster
# Mettre à jour: python ethos.py → 7 → 4
```

### Problème: "Rate limit exceeded"

**Solution:**
- Attendez quelques minutes
- Passez à un plan supérieur
- Utilisez le mode public (limité)

---

## 📚 Documentation complète

Pour plus d'informations, consultez:

- **`DNSDUMPSTER_GUIDE.md`** - Guide complet d'utilisation
- **`CHANGELOG_DNSDUMPSTER.md`** - Détails techniques
- **`demo_dnsdumpster.py`** - Exemples de code

---

## 🆘 Support

### Obtenir de l'aide

1. **Documentation**: Lisez les fichiers MD
2. **Demo**: Exécutez `python demo_dnsdumpster.py`
3. **Issues**: Ouvrez une issue sur GitHub
4. **Community**: Forum de discussion

### Rapporter un bug

```markdown
**Environnement:**
- OS: Windows 10 / Linux / macOS
- Python: 3.x.x
- Version ETHOS: 2.1

**Description:**
[Décrivez le problème]

**Commande:**
python ethos.py → 4 → example.com

**Erreur:**
[Collez le message d'erreur]
```

---

## 🎉 Remerciements

- **DNSDumpster** - Pour leur excellent service
- **Communauté OSINT** - Pour le feedback
- **Contributeurs** - Pour leurs contributions

---

## 📝 Changelog rapide

**v2.1 (2025)**
- ✨ Ajout de DNSDumpster
- 🔐 Chiffrement des clés API
- 🌐 Mode public sans API
- 📊 Énumération de sous-domaines
- 🐛 Corrections diverses

**v2.0 (2024)**
- Base ETHOS FINDER

---

## 🚀 Prochaines étapes

Après avoir testé DNSDumpster:

1. ✅ Configurez votre clé API
2. ✅ Testez sur vos domaines
3. ✅ Explorez l'énumération de sous-domaines
4. ✅ Consultez DNSDUMPSTER_GUIDE.md
5. ✅ Partagez vos retours

---

## 📄 Licence

MIT License - Voir LICENSE pour détails

## ⚠️ Disclaimer

**POUR USAGE ÉDUCATIF ET DÉFENSIF UNIQUEMENT**

Ce logiciel est fourni "tel quel" à des fins éducatives. L'utilisation non autorisée de cet outil sur des systèmes tiers peut être illégale. Les auteurs déclinent toute responsabilité en cas d'usage abusif.

---

**Version:** 2.1  
**Date:** 2025  
**Auteurs:** ETHOS Team  

**Happy Reconnaissance! 🔍🌐🛡️**