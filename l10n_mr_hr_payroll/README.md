# 🇲🇷 Mauritania - Payroll Module (Odoo 19)

## Description

Module de gestion de la paie conforme à la législation mauritanienne.

## ✨ Fonctionnalités

- ✅ Calcul automatique CNSS (1% employé / 15% employeur)
- ✅ Calcul automatique CNAM (1% employé / 3% employeur)
- ✅ Calcul ITS (Impôt sur Traitements et Salaires)
- ✅ Gestion des échelons et catégories
- ✅ Rapports officiels (CNSS, CNAM, ITS, États 1 & 2)
- ✅ Gestion des virements bancaires
- ✅ Bulletins de paie personnalisés

## 📦 Installation

```bash
# 1. Copier le module dans custom_addons
cd D:\dev_odoo\odoo-19.0\custom_addons\

# 2. Redémarrer Odoo
python odoo-bin -c conf.cfg

# 3. Activer le mode développeur

# 4. Apps > Rechercher "Mauritania" > Installer
```

## 🚀 Utilisation Rapide

### 1. Configuration initiale
```
Paie > Configuration > Paramètres
- Configurer les informations société (CNSS, CNAM)
```

### 2. Créer un employé
```
Employés > Créer
- Renseigner : CIN, CNSS, CNAM, Matricule
```

### 3. Créer un contrat
```
Contrats > Créer
- Choisir Catégorie et Échelon
- Ajouter primes et indemnités
```

### 4. Générer une fiche de paie
```
Paie > Fiches de paie > Créer
- Sélectionner employé et période
- Cliquer "Calculer"
- Valider
```

## 📊 Exemple Concret

### Employé : Ahmed Mohamed
```
Salaire base     : 200,000 MRU
Logement         :  50,000 MRU
Transport        :  20,000 MRU
─────────────────────────────
BRUT             : 270,000 MRU
CNSS (1%)        :  -2,700 MRU
CNAM (1%)        :  -2,700 MRU
ITS (calculé)    : -13,500 MRU
─────────────────────────────
NET À PAYER      : 251,100 MRU
```

## 📋 Rapports Disponibles

| Rapport | Description | Menu |
|---------|-------------|------|
| CNSS | Déclaration mensuelle | Paie > Rapports > CNSS |
| CNAM | Déclaration mensuelle | Paie > Rapports > CNAM |
| ITS | Déclaration fiscale | Paie > Rapports > ITS |
| État 1 | Récapitulatif mensuel | Paie > Rapports > État 1 |
| État 2 | Détails par employé | Paie > Rapports > État 2 |

## 🔧 Dépendances

- `hr_payroll` : Module paie de base Odoo
- `hr_contract` : Gestion des contrats (auto-installé)
- `hr` : RH de base (auto-installé)
- `account` : Comptabilité (optionnel)

## 📚 Documentation Complète

Consultez le [**Guide d'Utilisation Complet**](GUIDE_UTILISATION.md) pour :
- Tutoriel pas à pas détaillé
- Cas d'usage pratiques
- Workflow mensuel recommandé
- FAQ et bonnes pratiques

## 🏢 Adapté pour

- PME mauritaniennes
- Grandes entreprises
- Cabinets d'expertise comptable
- Administrations publiques

## ⚙️ Configuration Technique

### Structures de paie incluses
- Salaire mensuel
- Salaire journalier
- Salaire horaire

### Règles salariales
- Salaire de base
- Primes (logement, transport, repas, téléphone...)
- Heures supplémentaires
- Retenues (CNSS, CNAM, ITS, saisie)
- Charges patronales

## 🎯 Workflow Mensuel

```
┌─ Jour 1-20 ──────────────────────┐
│  Saisie présences & HS           │
└──────────────────────────────────┘
           ↓
┌─ Jour 21-25 ─────────────────────┐
│  Génération fiches de paie       │
│  Vérification & Validation       │
└──────────────────────────────────┘
           ↓
┌─ Jour 26-30 ─────────────────────┐
│  Virements bancaires             │
│  Distribution bulletins           │
└──────────────────────────────────┘
           ↓
┌─ Mois suivant (J+5 à J+10) ──────┐
│  Déclarations CNSS/CNAM/ITS      │
└──────────────────────────────────┘
```

## 💡 Exemple de Catégories/Échelons

### Catégories Standards
- Cadre Supérieur
- Cadre
- Agent de Maîtrise
- Employé
- Ouvrier

### Échelons Exemple (Cadre)
```
Cadre 1 : 150,000 MRU
Cadre 2 : 200,000 MRU
Cadre 3 : 300,000 MRU
```

## 🔐 Sécurité

- Accès par rôles (Manager RH, Employé RH, Comptable)
- Historique complet des modifications
- Sauvegarde automatique des bulletins
- Conformité RGPD pour données personnelles

## 🆘 Support

Pour toute question :
1. Consultez le [Guide d'Utilisation](GUIDE_UTILISATION.md)
2. Forum Odoo Community
3. Issues GitHub (si applicable)

## 📜 Licence

**OEEL-1** (Odoo Enterprise Edition License)

## 👨‍💻 Auteur

Odoo Community - Adapté pour la Mauritanie

## 🔄 Versions

| Version | Odoo | Status |
|---------|------|--------|
| 1.0 | 17.0 | ⚠️ Legacy |
| 1.0 | 19.0 | ✅ Actuelle |

## ⚡ Changements v19

### ✅ Améliorations
- ✔️ Import modernisé (`odoo.fields.Domain`)
- ✔️ Suppression modèle obsolète `hr.payroll.report`
- ✔️ Compatibilité Odoo 19
- ✔️ Performance optimisée

### 🗑️ Dépréciations
- `odoo.osv.expression` remplacé par `odoo.fields.Domain`
- Modèle `hr.payroll.report` → utilise mécanismes standards Odoo 19

## 📞 Contact

Pour questions techniques ou demandes de fonctionnalités, contactez l'équipe de développement.

---

**Made with ❤️ for Mauritanian Businesses**

🌟 Si ce module vous aide, n'hésitez pas à le partager !

