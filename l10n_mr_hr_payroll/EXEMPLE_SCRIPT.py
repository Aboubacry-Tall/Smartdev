#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXEMPLE DE SCRIPT : Automatisation de la paie mauritanienne avec Odoo 19
========================================================================

Ce script montre comment utiliser l'API Odoo pour automatiser
la création et le traitement des fiches de paie.

Usage:
    python EXEMPLE_SCRIPT.py

Note: Ce script est à usage pédagogique uniquement.
"""

# ============================================================================
# EXEMPLE 1 : Créer un employé avec informations mauritaniennes
# ============================================================================

def create_mauritanian_employee(env):
    """
    Crée un employé avec toutes les informations mauritaniennes requises
    """
    
    employee = env['hr.employee'].create({
        'name': 'Ahmed Mohamed Ould Abdallahi',
        'work_email': 'ahmed.mohamed@odoo.mr',
        'work_phone': '+222 45 25 12 34',
        
        # Informations mauritaniennes spécifiques
        'l10n_mr_matricule': 'MAT-2025-001',
        'l10n_mr_cin_number': '1234567890123',
        'l10n_mr_cnss_number': 'CNSS-2025-001',
        'l10n_mr_cimr_number': 'CIMR-2025-001',
        'l10n_mr_mut_number': 'MUT-2025-001',
        
        # Informations générales
        'department_id': env.ref('hr.dep_administration').id,
        'job_id': env.ref('hr.job_hrmanager').id,
        'resource_calendar_id': env.ref('resource.resource_calendar_std').id,
    })
    
    print(f"✅ Employé créé : {employee.name} (ID: {employee.id})")
    return employee


# ============================================================================
# EXEMPLE 2 : Créer une catégorie et des échelons
# ============================================================================

def create_categories_and_echelons(env):
    """
    Crée les catégories d'employés et les échelons correspondants
    """
    
    # Créer la catégorie
    category = env['hr.category'].create({
        'name': 'Cadre Technique',
    })
    
    print(f"✅ Catégorie créée : {category.name}")
    
    # Créer les échelons
    echelons_data = [
        {'name': 'Cadre Technique 1', 'salary': 150000},
        {'name': 'Cadre Technique 2', 'salary': 200000},
        {'name': 'Cadre Technique 3', 'salary': 300000},
    ]
    
    echelons = []
    for data in echelons_data:
        echelon = env['hr.echallon'].create({
            'name': data['name'],
            'salary': data['salary'],
            'category': category.id,
        })
        echelons.append(echelon)
        print(f"✅ Échelon créé : {echelon.name} - {echelon.salary:,} MRU")
    
    return category, echelons


# ============================================================================
# EXEMPLE 3 : Créer un contrat avec primes
# ============================================================================

def create_contract_with_allowances(env, employee, category, echelon):
    """
    Crée un contrat pour un employé avec toutes les primes mauritaniennes
    """
    
    contract = env['hr.version'].create({
        'name': f"Contrat - {employee.name}",
        'employee_id': employee.id,
        'category_id': category.id,
        'echallon_id': echelon.id,
        
        # Le salaire de base vient de l'échelon
        'wage': echelon.salary,
        
        # Primes et indemnités spécifiques Mauritanie
        'l10n_mr_hra': 50000,              # Allocation logement
        'l10n_mr_transport_exemption': 20000,  # Indemnité transport
        'l10n_mr_meal_allowance': 15000,   # Indemnité repas
        'l10n_mr_Telephone': 10000,        # Téléphone
        'l10n_mr_medical_allowance': 5000, # Allocation médicale
        'l10n_mr_Responsabilite': 25000,   # Prime de responsabilité
        
        # Dates
        'date_start': '2025-01-01',
        'state': 'open',
    })
    
    total_brut = (contract.wage + 
                  contract.l10n_mr_hra + 
                  contract.l10n_mr_transport_exemption +
                  contract.l10n_mr_meal_allowance +
                  contract.l10n_mr_Telephone +
                  contract.l10n_mr_medical_allowance +
                  contract.l10n_mr_Responsabilite)
    
    print(f"\n✅ Contrat créé pour {employee.name}")
    print(f"   Salaire de base : {contract.wage:,} MRU")
    print(f"   Primes totales  : {total_brut - contract.wage:,} MRU")
    print(f"   TOTAL BRUT      : {total_brut:,} MRU")
    
    return contract


# ============================================================================
# EXEMPLE 4 : Générer une fiche de paie
# ============================================================================

def generate_payslip(env, employee, date_from, date_to):
    """
    Génère une fiche de paie pour un employé
    """
    
    payslip = env['hr.payslip'].create({
        'employee_id': employee.id,
        'date_from': date_from,
        'date_to': date_to,
        'name': f"Paie {employee.name} - {date_from}",
    })
    
    # Calculer la paie
    payslip.compute_sheet()
    
    print(f"\n✅ Fiche de paie générée : {payslip.name}")
    print(f"   Période : {date_from} au {date_to}")
    
    # Afficher les détails
    print("\n📊 DÉTAILS DE LA PAIE:")
    for line in payslip.line_ids:
        if line.total != 0:
            sign = "+" if line.total > 0 else ""
            print(f"   {line.name:30s} : {sign}{line.total:>10,.0f} MRU")
    
    print(f"\n💰 SALAIRE NET : {payslip.net_wage:,.0f} MRU")
    
    return payslip


# ============================================================================
# EXEMPLE 5 : Générer un rapport CNSS
# ============================================================================

def generate_cnss_report(env, date_from, date_to):
    """
    Génère un rapport CNSS pour une période donnée
    """
    
    payslips = env['hr.payslip'].search([
        ('date_from', '>=', date_from),
        ('date_to', '<=', date_to),
        ('state', '=', 'done'),
    ])
    
    print(f"\n📋 RAPPORT CNSS - Période : {date_from} au {date_to}")
    print("=" * 70)
    print(f"{'Matricule':<15} {'Employé':<30} {'CNSS Employé':>12} {'CNSS Employeur':>12}")
    print("-" * 70)
    
    total_employee = 0
    total_employer = 0
    
    for payslip in payslips:
        # Calculer CNSS (1% employé, 15% employeur)
        cnss_employee = payslip.wage * 0.01
        cnss_employer = payslip.wage * 0.15
        
        total_employee += cnss_employee
        total_employer += cnss_employer
        
        print(f"{payslip.employee_id.l10n_mr_matricule:<15} "
              f"{payslip.employee_id.name:<30} "
              f"{cnss_employee:>12,.0f} "
              f"{cnss_employer:>12,.0f}")
    
    print("-" * 70)
    print(f"{'TOTAL':<45} {total_employee:>12,.0f} {total_employer:>12,.0f}")
    print("=" * 70)
    print(f"\n💼 TOTAL À VERSER À LA CNSS : {(total_employee + total_employer):,.0f} MRU")


# ============================================================================
# EXEMPLE 6 : Workflow complet mensuel
# ============================================================================

def monthly_payroll_workflow(env):
    """
    Exemple de workflow complet pour un mois
    """
    
    print("\n" + "=" * 70)
    print("🎯 WORKFLOW COMPLET : TRAITEMENT PAIE MENSUEL")
    print("=" * 70)
    
    # 1. Créer employé
    print("\n📍 ÉTAPE 1 : Création de l'employé")
    employee = create_mauritanian_employee(env)
    
    # 2. Créer catégorie et échelons
    print("\n📍 ÉTAPE 2 : Création catégories et échelons")
    category, echelons = create_categories_and_echelons(env)
    
    # 3. Créer contrat
    print("\n📍 ÉTAPE 3 : Création du contrat")
    contract = create_contract_with_allowances(env, employee, category, echelons[1])
    
    # 4. Générer fiche de paie
    print("\n📍 ÉTAPE 4 : Génération fiche de paie")
    payslip = generate_payslip(env, employee, '2025-01-01', '2025-01-31')
    
    # 5. Valider la fiche
    print("\n📍 ÉTAPE 5 : Validation de la fiche")
    payslip.action_payslip_done()
    print(f"✅ Fiche validée avec succès")
    
    # 6. Générer rapport CNSS
    print("\n📍 ÉTAPE 6 : Génération rapport CNSS")
    generate_cnss_report(env, '2025-01-01', '2025-01-31')
    
    print("\n" + "=" * 70)
    print("✅ WORKFLOW TERMINÉ AVEC SUCCÈS")
    print("=" * 70)


# ============================================================================
# EXEMPLE 7 : Calculer salaire net simplifié
# ============================================================================

def calculate_net_salary(gross_salary):
    """
    Calcul simplifié du salaire net mauritanien
    
    Args:
        gross_salary (float): Salaire brut en MRU
        
    Returns:
        dict: Détails du calcul
    """
    
    # Retenues
    cnss = gross_salary * 0.01  # 1%
    cnam = gross_salary * 0.01  # 1%
    
    # ITS progressif (simplifié)
    if gross_salary <= 50000:
        its = 0
    elif gross_salary <= 100000:
        its = (gross_salary - 50000) * 0.05
    elif gross_salary <= 200000:
        its = 2500 + (gross_salary - 100000) * 0.10
    else:
        its = 12500 + (gross_salary - 200000) * 0.15
    
    # Charges patronales
    cnss_employer = gross_salary * 0.15  # 15%
    cnam_employer = gross_salary * 0.03  # 3%
    
    total_deductions = cnss + cnam + its
    net_salary = gross_salary - total_deductions
    total_employer_charges = cnss_employer + cnam_employer
    
    return {
        'gross': gross_salary,
        'cnss_employee': cnss,
        'cnam_employee': cnam,
        'its': its,
        'total_deductions': total_deductions,
        'net': net_salary,
        'cnss_employer': cnss_employer,
        'cnam_employer': cnam_employer,
        'total_employer_charges': total_employer_charges,
        'total_cost': gross_salary + total_employer_charges,
    }


# ============================================================================
# EXEMPLE D'UTILISATION
# ============================================================================

def print_salary_example():
    """
    Affiche un exemple de calcul de salaire
    """
    
    print("\n" + "=" * 70)
    print("💰 EXEMPLE DE CALCUL DE SALAIRE")
    print("=" * 70)
    
    salaries = [150000, 200000, 300000, 500000]
    
    for salary in salaries:
        result = calculate_net_salary(salary)
        
        print(f"\n📊 Pour un salaire brut de {salary:,} MRU:")
        print(f"   {'Salaire brut':<30} : {result['gross']:>12,.0f} MRU")
        print(f"   {'CNSS employé (1%)':<30} : {result['cnss_employee']:>12,.0f} MRU")
        print(f"   {'CNAM employé (1%)':<30} : {result['cnam_employee']:>12,.0f} MRU")
        print(f"   {'ITS (progressif)':<30} : {result['its']:>12,.0f} MRU")
        print(f"   {'-' * 44}")
        print(f"   {'Total retenues':<30} : {result['total_deductions']:>12,.0f} MRU")
        print(f"   {'=' * 44}")
        print(f"   {'💵 SALAIRE NET':<30} : {result['net']:>12,.0f} MRU")
        print(f"\n   {'Charges patronales:':<30}")
        print(f"   {'  CNSS employeur (15%)':<30} : {result['cnss_employer']:>12,.0f} MRU")
        print(f"   {'  CNAM employeur (3%)':<30} : {result['cnam_employer']:>12,.0f} MRU")
        print(f"   {'-' * 44}")
        print(f"   {'🏢 COÛT TOTAL EMPLOYEUR':<30} : {result['total_cost']:>12,.0f} MRU")


# ============================================================================
# MAIN : Point d'entrée du script
# ============================================================================

if __name__ == '__main__':
    
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     MODULE PAIE MAURITANIE - EXEMPLES D'UTILISATION         ║
    ║                    Odoo 19.0                                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    print("\n⚠️  NOTE IMPORTANTE:")
    print("    Ce script contient des exemples pédagogiques.")
    print("    Pour utiliser dans Odoo, utilisez l'environnement Odoo:")
    print("    ")
    print("    from odoo import api, SUPERUSER_ID")
    print("    ")
    print("    with api.Environment.manage():")
    print("        env = api.Environment(cr, SUPERUSER_ID, {})")
    print("        monthly_payroll_workflow(env)")
    print()
    
    # Afficher l'exemple de calcul (sans connexion Odoo)
    print_salary_example()
    
    print("\n" + "=" * 70)
    print("📚 Pour plus d'informations, consultez :")
    print("   - GUIDE_UTILISATION.md : Guide complet étape par étape")
    print("   - README.md : Documentation rapide")
    print("=" * 70)
    print()

