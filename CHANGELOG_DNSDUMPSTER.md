# Changelog - Intégration DNSDumpster

## Version 2.1 - Ajout de DNSDumpster (2025)

### 🎉 Nouvelles fonctionnalités

#### 1. Module DNSDumpster (`tools/dnsdumpster_search.py`)
- ✅ Recherche de domaines via l'API DNSDumpster
- ✅ Récupération des enregistrements DNS (A, MX, TXT, NS, etc.)
- ✅ Découverte de sous-domaines
- ✅ Lookup public sans API (fallback)
- ✅ Énumération locale de sous-domaines
- ✅ Validation du format de domaine
- ✅ Gestion des erreurs et timeouts

#### 2. Interface CLI mise à jour (`ethos.py`)
- ✅ Nouveau menu option 4 : "🌐 Find by DOMAIN (DNSDumpster)"
- ✅ Validation du format de domaine
- ✅ Affichage des résultats formatés en JSON
- ✅ Option interactive d'énumération de sous-domaines
- ✅ Gestion des erreurs améliorée

#### 3. Gestion sécurisée de la clé API (`secure_config.py`)
- ✅ Support de la variable d'environnement `ETHOS_DNSDUMPSTER_KEY`
- ✅ Chiffrement automatique de la clé avec cryptography
- ✅ Nouvelles méthodes :
  - `set_dnsdumpster_key(key)` - Définir la clé
  - `get_dnsdumpster_key()` - Récupérer la clé
  - `remove_dnsdumpster_key()` - Supprimer la clé
- ✅ Mise à jour de `list_apis()` pour afficher le statut DNSDumpster

#### 4. Menu Settings étendu
- Option 4 : ADD DNSDumpster API Key
- Option 5 : REMOVE DNSDumpster API Key
- Option 6 : VIEW All Configuration (mise à jour)
- Affichage du statut de configuration DNSDumpster

#### 5. Documentation complète
- 📚 `DNSDUMPSTER_GUIDE.md` - Guide complet d'utilisation
- 📋 Instructions d'installation
- 💡 Exemples d'utilisation
- 🔧 Résolution de problèmes
- ⚖️ Considérations légales et éthiques

### 🔧 Améliorations techniques

#### Validation d'entrée
```python
def validate_domain_format(domain: str) -> bool:
    """Valide le format d'un domaine"""
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain) is not None
```

#### Gestion des erreurs API
- Timeout configuré à 15 secondes
- Messages d'erreur détaillés pour :
  - Authentication failed (401)
  - Rate limit exceeded (429)
  - Network timeouts
  - Invalid domain format

#### Mode fallback
Si aucune clé API n'est configurée :
1. Utilisation du lookup DNS standard
2. Résolution d'IP avec `socket.gethostbyname_ex()`
3. Message informatif pour l'utilisateur
4. Suggestion de configurer une clé API

### 📊 Fonctionnalités de recherche

#### Avec API DNSDumpster
```json
{
  "domain": "example.com",
  "dns_records": {
    "A": ["93.184.216.34"],
    "MX": ["mail.example.com"],
    "TXT": ["v=spf1 include:_spf.example.com ~all"]
  },
  "subdomains": [
    "www.example.com",
    "mail.example.com",
    "ftp.example.com"
  ],
  "ip_addresses": ["93.184.216.34"],
  "method": "api"
}
```

#### Sans API (Public lookup)
```json
{
  "domain": "example.com",
  "ip_addresses": ["93.184.216.34"],
  "note": "Public lookup - limited information",
  "method": "public"
}
```

#### Énumération de sous-domaines
```python
# Liste de 40+ sous-domaines communs testés
wordlist = [
    "www", "mail", "ftp", "webmail", "smtp",
    "pop", "ns1", "ns2", "cpanel", "autodiscover",
    "blog", "dev", "admin", "api", "staging",
    # ... et plus
]
```

### 🔒 Sécurité

#### Stockage sécurisé des clés
1. **Variable d'environnement** (Recommandé)
   ```bash
   export ETHOS_DNSDUMPSTER_KEY=your_key_here
   ```

2. **Fichier chiffré** (config.json)
   - Chiffrement AES avec Fernet
   - Clé de chiffrement stockée dans `.ethos_key`
   - Fichier caché sous Windows

3. **Fallback plaintext**
   - Si cryptography n'est pas installé
   - Avertissement affiché à l'utilisateur

#### Protection contre les abus
- Timeout de requête : 15 secondes
- Gestion du rate limiting (429)
- Messages d'erreur informatifs
- Validation stricte des entrées

### 📁 Structure des fichiers

```
EthosFinder/
├── ethos.py                      # ✨ Mis à jour
├── secure_config.py              # ✨ Mis à jour
├── config.py                     # Inchangé
├── tools/
│   ├── __init__.py              # ✨ Nouveau
│   ├── dnsdumpster_search.py   # ✨ Nouveau
│   ├── email_search.py
│   ├── phone_search.py
│   ├── handle_search.py
│   └── rapidapi_tools.py
├── DNSDUMPSTER_GUIDE.md         # ✨ Nouveau
├── CHANGELOG_DNSDUMPSTER.md     # ✨ Nouveau
└── requirements.txt
```

### 🎯 Cas d'usage

1. **Bug Bounty**
   - Découvrir des sous-domaines non documentés
   - Identifier les points d'entrée
   - Cartographier l'infrastructure

2. **Audit de sécurité**
   - Inventaire complet des actifs
   - Vérification de la configuration DNS
   - Détection de fuites d'information

3. **Red Team**
   - Reconnaissance passive
   - Identification de cibles
   - Planification d'attaque (avec autorisation)

4. **Blue Team**
   - Surveillance du périmètre
   - Détection d'actifs non autorisés
   - Vérification de conformité

### ⚠️ Limitations connues

1. **Mode public**
   - Informations limitées
   - Pas de découverte de sous-domaines via API
   - Basé uniquement sur DNS standard

2. **Énumération locale**
   - Limitée à une wordlist prédéfinie
   - Peut être lente (40+ requêtes DNS)
   - Certains sous-domaines peuvent être manqués

3. **API DNSDumpster**
   - Limites de taux selon le plan
   - Nécessite une inscription
   - Peut avoir un coût pour usage intensif

### 🐛 Corrections de bugs

- ✅ Gestion correcte des timeouts
- ✅ Validation stricte du format de domaine
- ✅ Messages d'erreur plus descriptifs
- ✅ Fallback graceful si API indisponible

### 📈 Performances

- ⚡ Lookup DNS rapide (< 1 seconde)
- ⚡ API DNSDumpster : 2-5 secondes
- 🐌 Énumération locale : 30-60 secondes (40+ domaines)
- 💾 Mémoire : Minimal (~10 MB)

### 🔮 Fonctionnalités futures

- [ ] Cache DNS local
- [ ] Export en CSV/XML
- [ ] Intégration avec Shodan
- [ ] Visualisation graphique de l'infrastructure
- [ ] Support de requêtes en batch
- [ ] Détection de changements DNS
- [ ] Intégration avec Certificate Transparency logs

### 📞 Support

**Problèmes connus :**
- Voir `DNSDUMPSTER_GUIDE.md` section "Résolution de problèmes"

**Rapporter un bug :**
```bash
# Inclure ces informations :
- Version Python
- Système d'exploitation
- Message d'erreur complet
- Commande exécutée
- Domaine testé (si possible)
```

### 🙏 Remerciements

- DNSDumpster pour leur excellent service
- La communauté OSINT
- Les contributeurs d'ETHOS FINDER

### 📄 Licence

Ce code reste sous licence MIT. Voir LICENSE pour détails.

### ⚖️ Disclaimer

**IMPORTANT :** Cette fonctionnalité est destinée uniquement à :
- L'éducation
- La sécurité défensive
- Les tests autorisés
- La recherche légitime

**L'utilisation non autorisée de cet outil peut être illégale.**

---

## Migration depuis v2.0

### Pour les utilisateurs existants :

1. **Mettre à jour le code :**
   ```bash
   git pull origin main
   ```

2. **Installer les nouvelles dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurer DNSDumpster :**
   ```bash
   python ethos.py
   # Option 7 (Settings) → Option 4 (Add DNSDumpster)
   ```

4. **Tester :**
   ```bash
   python ethos.py
   # Option 4 → Entrer "example.com"
   ```

### Pour les nouveaux utilisateurs :

Suivez le guide dans `QUICK_START.md` ou `README.md`

---

## Compatibilité

- ✅ Python 3.8+
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+, Debian, etc.)
- ✅ macOS 10.15+
- ✅ Compatible avec toutes les fonctionnalités existantes

---

## Tests

```bash
# Test de base
python -c "from tools import dnsdumpster_search; print(dnsdumpster_search.find_by_domain('google.com'))"

# Test avec énumération
python tools/dnsdumpster_search.py
# Entrer : google.com
# Énumérer : y
```

---

**Version :** 2.1  
**Date de release :** 2025  
**Contributeurs :** ETHOS Team  

**Happy Hacking! 🔍🌐**