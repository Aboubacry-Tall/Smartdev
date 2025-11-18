# 📘 Guide Pratique d'Utilisation - Module Paie Mauritanie (Odoo 19)

## 📋 Vue d'ensemble

Le module **Mauritania - Payroll** (l10n_mr_hr_payroll) permet de gérer la paie conforme à la législation mauritanienne avec :
- Gestion CNSS (Caisse Nationale de Sécurité Sociale)
- Gestion CNAM (Caisse Nationale d'Assurance Maladie)
- Calcul ITS (Impôt sur les Traitements et Salaires)
- Gestion des échelons et catégories d'employés
- Rapports de paie mauritaniens

---

## 🚀 Exemple Pratique Complet

### **Cas d'Usage : Société SOMAGAZ**
**Situation** : Vous êtes responsable RH de SOMAGAZ et devez gérer la paie de vos employés selon la législation mauritanienne.

---

## 📝 ÉTAPE 1 : Configuration Initiale

### 1.1 Installer le module
1. Accédez à **Apps** (Applications)
2. Recherchez "**Mauritania - Payroll**"
3. Cliquez sur **Installer**

### 1.2 Configurer la société
**Menu** : `Configuration > Paramètres > Paie`

Configurez les informations obligatoires :
```
- Nom société : SOMAGAZ
- Numéro CNSS Employeur : MR123456789
- Numéro CNAM Employeur : CNAM987654
- Devise : MRU (Ouguiya Mauritanien)
```

---

## 👥 ÉTAPE 2 : Créer les Catégories et Échelons

### 2.1 Créer une catégorie d'employé
**Menu** : `Paie > Configuration > Catégories`

**Exemple - Catégorie "Cadre"** :
```
Nom : Cadre
Code : CAD
Description : Personnel cadre de l'entreprise
```

### 2.2 Créer des échelons
**Menu** : `Paie > Configuration > Échelons`

**Exemple - Échelons pour Cadres** :
```
┌─────────────┬──────────────┬──────────────┐
│ Échelon     │ Catégorie    │ Salaire Base │
├─────────────┼──────────────┼──────────────┤
│ Cadre 1     │ Cadre        │ 150,000 MRU  │
│ Cadre 2     │ Cadre        │ 200,000 MRU  │
│ Cadre 3     │ Cadre        │ 300,000 MRU  │
└─────────────┴──────────────┴──────────────┘
```

**Comment créer** :
1. Cliquez sur **Nouveau**
2. Remplissez :
   - **Nom** : Cadre 1
   - **Catégorie** : Cadre
   - **Salaire** : 150000
3. **Enregistrer**

---

## 👤 ÉTAPE 3 : Créer un Employé

**Menu** : `Employés > Employés > Créer`

### Exemple : Employé Mohamed Ahmed

**Onglet Informations Générales** :
```
Nom : Ahmed Mohamed
Matricule : EMP001
Poste : Responsable Technique
Département : Technique
```

**Onglet Informations Privées - Section Mauritanie** :
```
📋 Informations Mauritanie
├─ N° CIN          : 1234567890123
├─ N° CNSS         : CNSS-2024-001
├─ N° CNAM         : CNAM-2024-001
├─ N° CIMR         : CIMR-2024-001
└─ Matricule       : MAT-001
```

**Comment remplir** :
1. Créer nouvel employé
2. Remplir les informations de base
3. Dans l'onglet "**Informations Privées**", trouver la section "**Mauritanie**"
4. Remplir tous les numéros obligatoires

---

## 📄 ÉTAPE 4 : Créer un Contrat

**Menu** : `Employés > Contrats > Créer`

### Exemple : Contrat de Mohamed Ahmed

**Informations principales** :
```
Employé : Ahmed Mohamed
Poste : Responsable Technique
Date début : 01/01/2025
Type de contrat : CDI
```

**Section Salaire et Primes** :
```
┌────────────────────────────┬─────────────┐
│ Élément                    │ Montant     │
├────────────────────────────┼─────────────┤
│ 💰 Salaire de base        │ 200,000 MRU │
│ 🏠 Allocation logement    │  50,000 MRU │
│ 🚗 Indemnité transport    │  20,000 MRU │
│ 🍽️  Indemnité repas       │  15,000 MRU │
│ 📞 Téléphone              │  10,000 MRU │
│ ⚕️  Allocation médicale    │   5,000 MRU │
├────────────────────────────┼─────────────┤
│ 📊 TOTAL BRUT             │ 300,000 MRU │
└────────────────────────────┴─────────────┘
```

**Comment remplir** :
1. **Catégorie** : Sélectionnez "Cadre"
2. **Échelon** : Sélectionnez "Cadre 2" → Le salaire se remplit automatiquement !
3. Remplissez les primes :
   - `l10n_mr_hra` (HRA/Logement) : 50000
   - `l10n_mr_transport_exemption` : 20000
   - `l10n_mr_meal_allowance` : 15000
   - `l10n_mr_Telephone` : 10000
   - `l10n_mr_medical_allowance` : 5000

---

## 💵 ÉTAPE 5 : Générer une Fiche de Paie

### 5.1 Créer la fiche de paie
**Menu** : `Paie > Fiches de paie > Créer`

**Configuration** :
```
Employé : Ahmed Mohamed
Période : Janvier 2025
Date de paiement : 31/01/2025
```

### 5.2 Calculer la paie
1. Cliquez sur **Calculer la fiche**
2. Le système calcule automatiquement :

```
┌─────────────────────────────────────────┐
│      📊 BULLETIN DE PAIE - JANVIER      │
├─────────────────────────────────────────┤
│ Employé : Ahmed Mohamed                 │
│ Matricule : EMP001                      │
│ CNSS : CNSS-2024-001                    │
├─────────────────────────────────────────┤
│ 💰 SALAIRE ET PRIMES                    │
│    Salaire de base        200,000 MRU   │
│    Allocation logement     50,000 MRU   │
│    Indemnité transport     20,000 MRU   │
│    Indemnité repas         15,000 MRU   │
│    Téléphone              10,000 MRU   │
│    Allocation médicale      5,000 MRU   │
├─────────────────────────────────────────┤
│    SALAIRE BRUT           300,000 MRU   │
├─────────────────────────────────────────┤
│ 📉 RETENUES                             │
│    CNSS (1%)               -3,000 MRU   │
│    CNAM (1%)               -3,000 MRU   │
│    ITS (Calculé)          -15,000 MRU   │
├─────────────────────────────────────────┤
│    TOTAL RETENUES         -21,000 MRU   │
├─────────────────────────────────────────┤
│ 💵 SALAIRE NET            279,000 MRU   │
├─────────────────────────────────────────┤
│ 🏢 CHARGES PATRONALES                   │
│    CNSS Employeur (15%)    45,000 MRU   │
│    CNAM Employeur (3%)      9,000 MRU   │
├─────────────────────────────────────────┤
│    TOTAL CHARGES           54,000 MRU   │
└─────────────────────────────────────────┘
```

### 5.3 Valider et payer
1. Vérifiez les montants
2. Cliquez sur **Confirmer**
3. Cliquez sur **Créer écriture comptable** (si module comptable activé)
4. Cliquez sur **Marquer comme payé**

---

## 📊 ÉTAPE 6 : Générer les Rapports Officiels

### 6.1 Rapport CNSS
**Menu** : `Paie > Rapports > Rapport CNSS`

**Période** : Sélectionnez le mois (ex: Janvier 2025)

**Le rapport génère** :
```
┌──────────────┬─────────────┬─────────────┬─────────────┐
│ Matricule    │ Nom         │ Salaire     │ CNSS        │
├──────────────┼─────────────┼─────────────┼─────────────┤
│ EMP001       │ Ahmed M.    │ 300,000     │ 3,000       │
│ EMP002       │ Fatima B.   │ 250,000     │ 2,500       │
├──────────────┼─────────────┼─────────────┼─────────────┤
│ TOTAL        │             │ 550,000     │ 5,500       │
└──────────────┴─────────────┴─────────────┴─────────────┘

Charges patronales CNSS : 82,500 MRU
TOTAL À PAYER À LA CNSS : 88,000 MRU
```

### 6.2 Rapport CNAM
**Menu** : `Paie > Rapports > Rapport CNAM`

### 6.3 Rapport ITS (Impôts)
**Menu** : `Paie > Rapports > Rapport ITS`

**Résumé mensuel** :
```
Total salaires bruts : 550,000 MRU
Total ITS retenu    :  35,000 MRU
À reverser au Trésor Public
```

### 6.4 État Récapitulatif Mensuel
**Menu** : `Paie > Rapports > État 1`

Génère le tableau récapitulatif officiel requis par l'administration mauritanienne.

---

## 🏦 ÉTAPE 7 : Gestion des Virements Bancaires

### 7.1 Préparer les virements
**Menu** : `Paie > Virements > Créer lot de virements`

**Configuration** :
```
Période : Janvier 2025
Compte bancaire : Compte SOMAGAZ - Banque XXX
```

Le système génère automatiquement :
```
┌──────────────┬────────────────┬────────────────┬────────────┐
│ Employé      │ N° Compte      │ Banque         │ Montant    │
├──────────────┼────────────────┼────────────────┼────────────┤
│ Ahmed M.     │ 1234567890     │ BNM            │ 279,000    │
│ Fatima B.    │ 0987654321     │ BMCI           │ 230,000    │
├──────────────┼────────────────┼────────────────┼────────────┤
│ TOTAL VIREMENTS                                │ 509,000    │
└──────────────┴────────────────┴────────────────┴────────────┘
```

### 7.2 Exporter pour la banque
- Format compatible avec les banques mauritaniennes
- Fichier CSV ou XML selon votre banque

---

## 📅 WORKFLOW MENSUEL RECOMMANDÉ

```
📆 CALENDRIER DE PAIE MENSUEL
════════════════════════════════════

📍 Jour 1-20 du mois
   └─ Saisie des présences, absences, heures supplémentaires
   
📍 Jour 21-25 du mois
   └─ Génération des fiches de paie
   └─ Vérification et validation
   
📍 Jour 26-28 du mois
   └─ Création des écritures comptables
   └─ Préparation des virements
   
📍 Jour 29-30 du mois
   └─ Exécution des virements bancaires
   └─ Distribution des bulletins
   
📍 Jour 5-10 du mois suivant
   └─ Génération rapports CNSS/CNAM/ITS
   └─ Déclarations et paiements aux organismes
```

---

## 🎯 CAS D'USAGE SPÉCIFIQUES

### Cas 1 : Heures Supplémentaires
```python
# Dans la fiche de paie, ajouter une ligne de saisie :
Type : Heures supplémentaires
Quantité : 20 heures
Taux : 125% (majoration légale)
Montant calculé automatiquement
```

### Cas 2 : Prime Exceptionnelle
```python
# Dans le contrat ou la fiche de paie :
Prime de performance : 50,000 MRU
Prime de fin d'année : 100,000 MRU
→ Soumises à ITS mais exonérées de CNSS si ponctuelles
```

### Cas 3 : Avance sur Salaire
```python
# Menu : Paie > Avances
Montant avance : 50,000 MRU
Date : 15/01/2025
→ Sera déduite automatiquement sur la paie de fin de mois
```

### Cas 4 : Saisie sur Salaire
```python
# Dans le contrat :
l10n_mr_saisie : Montant de la saisie ordonnée par justice
→ Déduit automatiquement chaque mois
```

---

## 🔧 PARAMÈTRES AVANCÉS

### Configuration des taux
**Menu** : `Paie > Configuration > Paramètres de règles`

**Taux mauritaniens standards** :
```
┌─────────────────────┬────────────┬─────────────┐
│ Organisme           │ Employé    │ Employeur   │
├─────────────────────┼────────────┼─────────────┤
│ CNSS                │ 1%         │ 15%         │
│ CNAM                │ 1%         │ 3%          │
│ ITS (Progressif)    │ 0-15%      │ -           │
└─────────────────────┴────────────┴─────────────┘
```

**Barème ITS** :
```
0 - 50,000 MRU       → 0%
50,001 - 100,000     → 5%
100,001 - 200,000    → 10%
200,001 et plus      → 15%
```

---

## ⚠️ POINTS IMPORTANTS

### ✅ À FAIRE
- ✔️ Vérifier les numéros CNSS/CNAM de chaque employé
- ✔️ Valider les fiches avant le 25 du mois
- ✔️ Archiver les bulletins de paie (légalement requis)
- ✔️ Faire les déclarations sociales dans les délais

### ❌ À NE PAS FAIRE
- ❌ Ne pas modifier une fiche validée et payée
- ❌ Ne pas oublier les déclarations trimestrielles
- ❌ Ne pas mélanger les périodes de paie
- ❌ Ne pas supprimer les anciennes fiches

---

## 📞 SUPPORT ET RESSOURCES

### Documentation
- Manuel utilisateur complet : `/docs/`
- Vidéos tutoriels : [À venir]

### Aide en ligne
- Forum communauté Odoo
- Support technique : support@somagaz.mr

### Législation
- Code du Travail Mauritanien 2023
- Décrets CNSS/CNAM en vigueur
- Loi de finances 2025

---

## 🎓 EXERCICE PRATIQUE

### Exercice : Calculer la paie d'un nouvel employé

**Données** :
```
Nom : Aminata Sall
Poste : Comptable
Catégorie : Cadre
Échelon : Cadre 1
Salaire base : 150,000 MRU
Prime logement : 40,000 MRU
Prime transport : 15,000 MRU
```

**Questions** :
1. Créer la fiche employé avec les informations mauritaniennes
2. Créer le contrat avec les primes
3. Générer la fiche de paie de Janvier 2025
4. Calculer le salaire net
5. Générer le rapport CNSS

**Solution** : Suivez les étapes 3, 4 et 5 de ce guide !

---

## 📈 STATISTIQUES UTILES

Le module permet de générer :
- **Masse salariale mensuelle**
- **Évolution des charges sociales**
- **Coût moyen par employé**
- **Répartition par catégorie/département**

**Menu** : `Paie > Reporting > Analyses`

---

## 🌟 BONNES PRATIQUES

1. **Organisation** : Créez les catégories et échelons avant les contrats
2. **Vérification** : Double-vérifiez les calculs le premier mois
3. **Archivage** : Exportez les bulletins mensuellement
4. **Formation** : Formez plusieurs personnes sur le système
5. **Backup** : Sauvegardez la base de données régulièrement

---

**Version** : 1.0 pour Odoo 19
**Dernière mise à jour** : Octobre 2024
**Module** : l10n_mr_hr_payroll

---

*Ce guide a été créé pour faciliter l'utilisation du module de paie mauritanienne dans Odoo 19.*

