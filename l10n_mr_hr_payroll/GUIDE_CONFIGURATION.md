# 🔧 Guide de Configuration - Module Paie Mauritanie

## 📋 Table des Matières
1. [Configuration Générale de la Société](#1-configuration-générale-de-la-société)
2. [Configuration Paie Mauritanienne](#2-configuration-paie-mauritanienne)
3. [Vérification de la Configuration](#3-vérification-de-la-configuration)

---

## 1️⃣ Configuration Générale de la Société

### **Étape 1.1 : Accéder aux Paramètres Généraux**

```
Menu Principal → Configuration → Paramètres (Settings)
```

OU cliquez sur l'icône **⚙️ Paramètres** en haut à droite

### **Étape 1.2 : Section Entreprises (Companies)**

Dans la page de paramètres, cherchez la section **"Entreprises"** :

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️  PARAMÈTRES                                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🏢 Entreprises                                         │
│     Configurer les informations de votre entreprise     │
│                                                          │
│     [Configurer les entreprises] ← CLIQUEZ ICI          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### **Étape 1.3 : Modifier votre Société**

1. Cliquez sur **"Configurer les entreprises"**
2. Sélectionnez votre société (ex: **SOMAGAZ**)
3. Cliquez sur **Modifier** (bouton en haut à droite)

### **Étape 1.4 : Remplir les Informations de Base**

```
┌─────────────────────────────────────────────────────────┐
│  SOMAGAZ                                    [Modifier]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📝 Informations Générales                              │
│  ├─ Nom de la société : SOMAGAZ                         │
│  ├─ Adresse          : Nouakchott, Mauritanie          │
│  ├─ Téléphone        : +222 45 25 XX XX                │
│  ├─ Email            : contact@somagaz.mr               │
│  ├─ Site web         : www.somagaz.mr                   │
│  └─ TVA/NIF          : MR123456789                      │
│                                                          │
│  💰 Devise                                              │
│  └─ Devise           : MRU (Ouguiya Mauritanien)        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Cliquez sur [Enregistrer]** quand c'est terminé.

---

## 2️⃣ Configuration Paie Mauritanienne

### **Étape 2.1 : Accéder aux Paramètres de Paie**

Il y a **DEUX FAÇONS** d'accéder aux paramètres :

#### **🔹 Méthode 1 : Via le Menu Paie**

```
Menu Principal → Paie → Configuration → Paramètres
```

#### **🔹 Méthode 2 : Via les Paramètres Généraux**

```
Configuration → Paramètres → cherchez "Paie"
```

### **Étape 2.2 : Localiser la Section "Mauritania Localization"**

Dans la page des paramètres de paie, **FAITES DÉFILER VERS LE BAS** jusqu'à trouver :

```
┌─────────────────────────────────────────────────────────┐
│  ⚙️  PARAMÈTRES DE LA PAIE                              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ... (autres sections) ...                              │
│                                                          │
│  ╔════════════════════════════════════════════════════╗ │
│  ║  🇲🇷 Mauritania Localization                       ║ │
│  ╠════════════════════════════════════════════════════╣ │
│  ║                                                    ║ │
│  ║  Company Information                               ║ │
│  ║  Official Company Information                      ║ │
│  ║                                                    ║ │
│  ║  ┌───────────────────────────────────────────────┐║ │
│  ║  │ Employer Contribution : [______________%]     │║ │
│  ║  │                                               │║ │
│  ║  │ Social Security Organization : [____________]│║ │
│  ║  │                                               │║ │
│  ║  │ Collective Agreement : [___________________]│║ │
│  ║  └───────────────────────────────────────────────┘║ │
│  ╚════════════════════════════════════════════════════╝ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### **Étape 2.3 : Remplir les Champs Mauritaniens**

Voici ce que vous devez renseigner pour **SOMAGAZ** :

```
╔══════════════════════════════════════════════════════════╗
║  📋 INFORMATIONS À REMPLIR                               ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  1️⃣  Employer Contribution (Contribution Employeur)     ║
║      └─ Valeur : 18%                                     ║
║      └─ Description : Total des charges patronales      ║
║                       (CNSS 15% + CNAM 3%)               ║
║                                                          ║
║  2️⃣  Social Security Organization                       ║
║      └─ Valeur : CNSS-MR-2025-SOMAGAZ                   ║
║      └─ Description : Numéro d'enregistrement CNSS      ║
║                       de votre société                   ║
║                                                          ║
║  3️⃣  Collective Agreement                               ║
║      └─ Valeur : Convention Collective du Gaz           ║
║      └─ Description : Nom de votre convention           ║
║                       collective (si applicable)         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
```

### **Étape 2.4 : Exemple Complet pour SOMAGAZ**

```
┌───────────────────────────────────────────────────────────┐
│  🇲🇷 Mauritania Localization                             │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  Company Information                                      │
│  Official Company Information                             │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                                                     │ │
│  │  Employer Contribution                              │ │
│  │  ┌─────┐                                            │ │
│  │  │  18 │ %                                          │ │
│  │  └─────┘                                            │ │
│  │  💡 (15% CNSS + 3% CNAM)                           │ │
│  │                                                     │ │
│  │  Social Security Organization                       │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │ CNSS-MR-2025-SOMAGAZ                         │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  💡 Votre numéro CNSS employeur                    │ │
│  │                                                     │ │
│  │  Collective Agreement                               │ │
│  │  ┌──────────────────────────────────────────────┐  │ │
│  │  │ Convention Collective Pétrolière/Gazière     │  │ │
│  │  └──────────────────────────────────────────────┘  │ │
│  │  💡 Si applicable                                  │ │
│  │                                                     │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  [Enregistrer] ← N'OUBLIEZ PAS DE SAUVEGARDER !         │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## 3️⃣ Vérification de la Configuration

### **Checklist de Vérification ✅**

Après avoir sauvegardé, vérifiez que tout est en place :

```
✅ Checklist Configuration SOMAGAZ
═══════════════════════════════════════════════════════════

□ Informations Générales
  ✅ Nom société : SOMAGAZ
  ✅ Adresse complète renseignée
  ✅ Téléphone et email renseignés
  ✅ NIF/TVA renseigné
  ✅ Devise : MRU (Ouguiya)

□ Paie Mauritanienne
  ✅ Employer Contribution : 18%
  ✅ Numéro CNSS employeur renseigné
  ✅ Convention collective (si applicable)

□ Configuration Paie de Base
  ✅ Structure de paie créée
  ✅ Règles salariales activées
  ✅ Périodes de paie configurées
```

---

## 📸 CAPTURE D'ÉCRAN : Où Trouver les Paramètres

### **Navigation Visuelle**

```
┌─────────────────────────────────────────────────────────┐
│  ODOO                                     👤 Admin ▼     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌────────────────┐     │
│  │ Paie │  │  RH  │  │Compta│  │⚙️ Configuration│ ◄───┐│
│  └──────┘  └──────┘  └──────┘  └────────────────┘     ││
│                                          │              ││
│                                          ▼              ││
│                                  ┌──────────────┐      ││
│                                  │ Paramètres   │ ◄────┘│
│                                  └──────────────┘       │
│                                          │              │
│  ┌───────────────────────────────────────▼───────────┐ │
│  │                                                    │ │
│  │  PAGE DES PARAMÈTRES                              │ │
│  │                                                    │ │
│  │  🏢 Entreprises                                   │ │
│  │  📊 Comptabilité                                  │ │
│  │  💰 Paie  ◄──── FAITES DÉFILER ICI               │ │
│  │     │                                             │ │
│  │     ├─ Configuration générale                     │ │
│  │     ├─ Structures de paie                         │ │
│  │     └─ 🇲🇷 Mauritania Localization  ◄─── C'EST ICI│ │
│  │                                                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Accès Rapide par URL

Si vous ne trouvez pas les paramètres dans le menu, vous pouvez y accéder directement :

```
http://localhost:8072/web#action=base_setup.action_general_configuration
```

Ou pour les paramètres de paie :

```
http://localhost:8072/web#action=hr_payroll.action_hr_payroll_configuration
```

---

## 💡 ASTUCES IMPORTANTES

### ⚠️ Problème : Je ne vois pas "Mauritania Localization"

**Solution** :
1. Vérifiez que le module `l10n_mr_hr_payroll` est **installé**
2. Vérifiez que le module `hr_payroll` est **installé**
3. Actualisez la page (F5)
4. Videz le cache du navigateur

### 🔍 Comment Vérifier si le Module est Installé ?

```
Menu → Apps (Applications)
Recherchez : "Mauritania"

┌────────────────────────────────────────┐
│  🇲🇷 Mauritania - Payroll             │
│  ✅ INSTALLÉ                           │
│  Version 1.0 pour Odoo 19             │
└────────────────────────────────────────┘
```

Si vous voyez ❌ **DÉSINSTALLÉ**, cliquez sur **[Installer]**

---

## 📝 Configuration Avancée (Optionnel)

### Configuration Comptable

Si vous avez le module **Comptabilité** activé :

**Menu** : `Comptabilité → Configuration → Paramètres`

```
Comptes de Paie
├─ Compte salaires à payer   : 421000
├─ Compte charges sociales    : 431000
├─ Compte CNSS employeur      : 431100
└─ Compte CNAM employeur      : 431200
```

---

## 🆘 Aide Supplémentaire

### Je ne trouve toujours pas les paramètres !

**Option 1 : Recherche Globale**

En haut à droite, cliquez sur 🔍 et tapez :
```
"Configuration" ou "Paramètres" ou "Settings"
```

**Option 2 : Mode Développeur**

1. Activez le mode développeur :
   - Menu → Paramètres
   - Cliquez sur "Activer le mode développeur"

2. Puis accédez à :
   - Menu → Technique → Paramètres → Configuration

**Option 3 : Demandez de l'Aide**

Si vous êtes bloqué, consultez :
- Le fichier `GUIDE_UTILISATION.md`
- Le fichier `README.md`
- La communauté Odoo

---

## ✅ Validation Finale

Pour confirmer que tout fonctionne :

### Test 1 : Créer un Employé
```
Employés → Créer
└─ Vérifiez que les champs mauritaniens sont visibles :
    - N° CIN
    - N° CNSS
    - N° CNAM
    - Matricule
```

### Test 2 : Créer un Contrat
```
Contrats → Créer
└─ Vérifiez que les primes mauritaniennes sont visibles :
    - Allocation logement (HRA)
    - Indemnité transport
    - Indemnité repas
    - etc.
```

### Test 3 : Générer une Fiche de Paie
```
Paie → Fiches de paie → Créer
└─ Le calcul doit inclure CNSS, CNAM et ITS automatiquement
```

---

## 📞 Support

Si vous avez des questions sur la configuration :
- 📧 Email : support@somagaz.mr
- 📖 Documentation : Consultez GUIDE_UTILISATION.md
- 🌐 Forum : Community Odoo

---

**Dernière mise à jour** : Octobre 2024  
**Version** : 1.0 pour Odoo 19  
**Module** : l10n_mr_hr_payroll

---

**🎉 Félicitations !**  
Votre système de paie mauritanienne est maintenant configuré et prêt à l'emploi !

