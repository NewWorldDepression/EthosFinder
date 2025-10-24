# DNSDumpster Integration Guide

Guide complet pour utiliser la fonctionnalité DNSDumpster dans ETHOS FINDER v2.

---

## 📋 Table des matières

1. [Qu'est-ce que DNSDumpster ?](#quest-ce-que-dnsdumpster-)
2. [Installation et Configuration](#installation-et-configuration)
3. [Obtenir une clé API](#obtenir-une-clé-api)
4. [Utilisation](#utilisation)
5. [Exemples](#exemples)
6. [Résolution de problèmes](#résolution-de-problèmes)

---

## Qu'est-ce que DNSDumpster ?

DNSDumpster est un service de reconnaissance de domaines qui permet de :
- 🔍 Découvrir les sous-domaines
- 📊 Récupérer les enregistrements DNS (A, MX, TXT, etc.)
- 🗺️ Cartographier l'infrastructure réseau
- 🔐 Identifier les points d'entrée potentiels

**Cas d'usage :**
- Audit de sécurité
- Reconnaissance passive
- Cartographie réseau
- Bug bounty
- Red team / Blue team

---

## Installation et Configuration

### 1. Prérequis

Assurez-vous d'avoir installé toutes les dépendances :

```bash
pip install -r requirements.txt
```

### 2. Configuration de la clé API

#### Option A : Via l'interface CLI (Recommandé)

```bash
python ethos.py
# Sélectionnez : 7 (SETTINGS)
# Puis : 4 (ADD DNSDumpster API Key)
# Entrez votre clé API
```

#### Option B : Variable d'environnement (Plus sécurisé)

```bash
# Windows
set ETHOS_DNSDUMPSTER_KEY=votre_clé_api_ici

# Linux/Mac
export ETHOS_DNSDUMPSTER_KEY=votre_clé_api_ici
```

#### Option C : Configuration manuelle

Créez ou modifiez `config.json` :

```json
{
  "dnsdumpster_api_key": "votre_clé_api_ici",
  "rapidapi_key": "",
  "rapidapi_hosts": {}
}
```

**Note :** Si vous utilisez `secure_config.py`, la clé sera automatiquement chiffrée.

---

## Obtenir une clé API

### Inscription DNSDumpster

1. **Visitez** : https://dnsdumpster.com/api (ou le site officiel)
2. **Créez un compte** ou connectez-vous
3. **Générez une clé API** dans votre tableau de bord
4. **Copiez la clé** et sauvegardez-la en sécurité

### Plans tarifaires

| Plan | Limites | Prix |
|------|---------|------|
| **Free** | 10 requêtes/jour | Gratuit |
| **Basic** | 100 requêtes/jour | ~5$/mois |
| **Pro** | 1000 requêtes/jour | ~20$/mois |
| **Enterprise** | Illimité | Sur devis |

**Note :** Les tarifs peuvent varier. Consultez le site officiel.

---

## Utilisation

### Recherche de base

1. Lancez ETHOS FINDER :
```bash
python ethos.py
```

2. Sélectionnez l'option **4** (Find by DOMAIN)

3. Entrez un domaine :
```
Enter domain (e.g., example.com): example.com
```

4. Les résultats s'affichent automatiquement

### Énumération de sous-domaines

Si aucune clé API n'est configurée, vous pouvez utiliser l'énumération locale :

```
Would you like to enumerate subdomains? (y/N): y
```

Cette fonction teste une liste de sous-domaines communs.

---

## Exemples

### Exemple 1 : Recherche simple

```bash
$ python ethos.py
# Sélectionnez 4 (Domain)
Enter domain: google.com

[*] Starting domain reconnaissance...
[+] DNSDumpster API key found - using API search
[i] Querying DNSDumpster API for domain: google.com
[+] API search completed successfully

RESULTS:
{
  "domain": "google.com",
  "dns_records": {
    "A": ["142.250.185.46"],
    "MX": ["smtp.google.com"],
    "TXT": ["v=spf1 include:_spf.google.com ~all"]
  },
  "subdomains": [
    "www.google.com",
    "mail.google.com",
    "drive.google.com"
  ],
  "method": "api"
}
```

### Exemple 2 : Sans clé API (lookup public)

```bash
Enter domain: example.com

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
```

### Exemple 3 : Énumération de sous-domaines

```bash
Enter domain: example.com
[*] Starting domain reconnaissance...

Would you like to enumerate subdomains? (y/N): y

[i] Enumerating subdomains for example.com...
[i] Testing 40 common subdomain names...
  [+] Found: www.example.com
  [+] Found: mail.example.com
  [+] Found: ftp.example.com
[+] Found 3 active subdomains

SUBDOMAINS FOUND:
  - www.example.com
  - mail.example.com
  - ftp.example.com
```

---

## Résolution de problèmes

### ❌ "Invalid domain format"

**Problème :** Le format du domaine est invalide.

**Solution :**
```bash
# ✅ Correct
example.com
subdomain.example.com
test.co.uk

# ❌ Incorrect
http://example.com  # Pas d'URL
example            # TLD manquant
example.          # Point final invalide
```

### ❌ "Authentication failed"

**Problème :** Clé API invalide ou expirée.

**Solutions :**
1. Vérifiez que la clé est correctement copiée
2. Régénérez une nouvelle clé sur DNSDumpster
3. Vérifiez votre abonnement

```bash
# Vérifier la configuration actuelle
python ethos.py
# 7 → 6 (VIEW All Configuration)
```

### ❌ "Rate limit exceeded"

**Problème :** Trop de requêtes en peu de temps.

**Solutions :**
1. Attendez avant de refaire une requête
2. Passez à un plan supérieur
3. Utilisez le mode public (limité)

### ❌ "Request timed out"

**Problème :** Le serveur ne répond pas.

**Solutions :**
1. Vérifiez votre connexion Internet
2. Réessayez plus tard
3. Vérifiez le pare-feu

### ❌ Module not found

**Problème :** Module `dnsdumpster_search` introuvable.

**Solution :**
```bash
# Vérifiez que le fichier existe
ls tools/dnsdumpster_search.py

# Réinstallez les dépendances
pip install -r requirements.txt
```

---

## Sécurité et bonnes pratiques

### 🔒 Protection de la clé API

1. **Ne commitez JAMAIS** votre clé API dans Git
2. **Utilisez** les variables d'environnement en production
3. **Activez** le chiffrement avec `cryptography`
4. **Renouvelez** régulièrement vos clés

### 📜 Utilisation légale et éthique

✅ **Autorisé :**
- Tests sur vos propres domaines
- Bug bounty avec autorisation
- Audit de sécurité contractuel
- Recherche académique

❌ **Interdit :**
- Scanning sans autorisation
- Attaques ou exploitation
- Violation de confidentialité
- Usage commercial non autorisé

### ⚖️ Conformité légale

Respectez :
- Le Computer Fraud and Abuse Act (CFAA) aux USA
- La GDPR en Europe
- Les lois locales sur la cybersécurité
- Les conditions d'utilisation de DNSDumpster

---

## API DNSDumpster - Référence

### Endpoints disponibles

```
POST https://api.dnsdumpster.com/v1/search
```

**Headers requis :**
```
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

**Body :**
```json
{
  "domain": "example.com"
}
```

**Réponse (exemple) :**
```json
{
  "domain": "example.com",
  "dns_records": {
    "A": ["93.184.216.34"],
    "AAAA": ["2606:2800:220:1:248:1893:25c8:1946"],
    "MX": ["mail.example.com"],
    "NS": ["ns1.example.com", "ns2.example.com"],
    "TXT": ["v=spf1 ..."]
  },
  "subdomains": [
    "www.example.com",
    "mail.example.com"
  ]
}
```

---

## Intégration avec d'autres outils

### Avec Nmap

```bash
# 1. Récupérer les sous-domaines avec ETHOS
python ethos.py
# Option 4 → Entrer le domaine

# 2. Scanner avec Nmap
nmap -sV subdomain.example.com
```

### Avec Metasploit

```bash
# 1. Énumérer avec ETHOS
python ethos.py

# 2. Utiliser dans Metasploit
msfconsole
use auxiliary/gather/dns_enum
set DOMAIN example.com
run
```

### Export pour analyse

```python
# Script personnalisé
import json
from tools import dnsdumpster_search

result = dnsdumpster_search.find_by_domain("example.com")

# Sauvegarder en JSON
with open("scan_results.json", "w") as f:
    json.dump(result, f, indent=2)
```

---

## FAQ

**Q: DNSDumpster est-il gratuit ?**  
R: Oui, il existe un plan gratuit avec des limites de requêtes.

**Q: Puis-je utiliser DNSDumpster sans clé API ?**  
R: Oui, ETHOS FINDER propose un mode de lookup public basique.

**Q: Les résultats sont-ils en temps réel ?**  
R: Oui, pour les requêtes API. Le mode public peut avoir un léger délai.

**Q: Puis-je scanner plusieurs domaines ?**  
R: Oui, mais respectez les limites de votre plan API.

**Q: Comment signaler un bug ?**  
R: Ouvrez une issue sur GitHub avec les détails.

---

## Ressources supplémentaires

- 📚 [Documentation officielle DNSDumpster](https://dnsdumpster.com/docs)
- 🛠️ [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- 🎓 [OSINT Framework](https://osintframework.com/)
- 💬 [Community Forum](https://github.com/yourusername/EthosFinder/discussions)

---

## Changelog

### Version 2.0 (2025)
- ✨ Ajout de l'intégration DNSDumpster
- 🔐 Support du chiffrement des clés API
- 🌐 Mode public sans API
- 📊 Énumération de sous-domaines
- 🐛 Corrections et améliorations

---

**Licence:** MIT  
**Auteur:** ETHOS Team  
**Contact:** support@ethosfinder.com  
**Disclaimer:** Pour usage éducatif et défensif uniquement

---

**Happy Reconnaissance! 🔍🛡️**