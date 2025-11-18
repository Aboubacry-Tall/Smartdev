from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class CustomSalaryReport(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.custom_salary_report_banques'
    _description = 'Custom Salary Report'

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     docs = self.env['custom.salary.report.wizard'].browse(docids)
    #     bank_ids = {}
    #     for doc in docs:
    #         for payslip in self.env['hr.payslip'].search([('date_from', '>=', doc.date_start), ('date_to', '<=', doc.date_end)]):
    #             bank = payslip.employee_id.bank_account_id.bank_id
    #             if bank not in bank_ids:
    #                 bank_ids[bank] = []
    #             bank_ids[bank].append(payslip)

    #     bank_data = []
    #     print(" bank_ids.items()", bank_ids.items())
    #     for bank, payslips in bank_ids.items():
    #         _logger.debug("Bank: %s, Payslips: %s", bank.name, payslips)
    #         bank_data.append({
    #             'name': bank.name,
    #             'payslip_ids': payslips,
    #         })

    #     return {
    #         'doc_ids': docids,
    #         'doc_model': 'custom.salary.report.wizard',
    #         'docs': docs,
    #         'bank_ids': bank_data,
    #         'time': fields.Datetime.now(),
    #     }
        
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.payslip.run'].browse(docids)
        bank_data = {}
        for doc in docs:
            for payslip in self.env['hr.payslip'].search([('date_from', '>=', doc.date_start), ('date_to', '<=', doc.date_end)]):
                bank = payslip.employee_id.primary_bank_account_id.bank_id
                if bank.id not in bank_data:
                    bank_data[bank.id] = {'bank': bank, 'payslips': []}
                bank_data[bank.id]['payslips'].append(payslip)
        
        bank_data_list = [{'bank': bank_info['bank'], 'payslips': bank_info['payslips']} for bank_info in bank_data.values()]
        
        virements = self.env['hr.virement'].search([], limit=1)
        virement = virements[0] if virements else None

        if not virements:
            raise UserError(_("Veuillez saisir les informations de virement dans les paramètres"))
    
        else :
            return {
                'doc_ids': docids,
                'doc_model': 'custom.salary.report.wizard',
                'docs': docs,
                'bank_data': bank_data_list,
                'virement': virement,
                'time': fields.Datetime.now(),
            }


class CustomSalaryReportPayslkip(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.custom_salary_report__payslip_banques'

    


    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.payslip'].browse(docids)
        bank_data = {}

        for payslip in docs:
            bank = payslip.employee_id.primary_bank_account_id.bank_id
            if bank.id not in bank_data:
                bank_data[bank.id] = {'bank': bank, 'payslips': []}
            bank_data[bank.id]['payslips'].append(payslip)

        bank_data_list = [{'bank': bank_info['bank'], 'payslips': bank_info['payslips']}
                          for bank_info in bank_data.values()]
        
        virements = self.env['hr.virement'].search([], limit=1)
        virement = virements[0] if virements else None

        _logger.info(f'Bank data: {bank_data_list}')

        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'docs': docs,
            'bank_data': bank_data_list,
            'virement': virement,
            'time': fields.Datetime.now(),
        }

class ReportPayslipIts(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.report_payslip_its'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Fetch payslips based on the provided docids
        docs = self.env['hr.payslip'].browse(docids)
        employee_data = {}

        # Organize payslips by employee
        for payslip in docs:
            employee = payslip.employee_id
            if employee.id not in employee_data:
                employee_data[employee.id] = {
                    'employee': employee,
                    'payslips': []
                }
            employee_data[employee.id]['payslips'].append(payslip)

        # Prepare the data in a format that avoids duplication
        employee_data_list = list(employee_data.values())

        _logger.info(f'Employee data: {employee_data_list}')
        
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'employee_data': employee_data_list,
            'time': fields.Datetime.now(),
        }

class ReportPayslipCnam(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.report_payslip_cnam'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Fetch payslips based on the provided docids
        docs = self.env['hr.payslip'].browse(docids)
        employee_data = {}

        # Organize payslips by employee
        for payslip in docs:
            employee = payslip.employee_id
            if employee.id not in employee_data:
                employee_data[employee.id] = {
                    'employee': employee,
                    'payslips': []
                }
            employee_data[employee.id]['payslips'].append(payslip)

        # Prepare the data in a format that avoids duplication
        employee_data_list = list(employee_data.values())

        _logger.info(f'Employee data: {employee_data_list}')
        
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'employee_data': employee_data_list,
            'time': fields.Datetime.now(),
        }

class ReportPayslipCnss(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.report_payslip_cnss'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Fetch payslips based on the provided docids
        docs = self.env['hr.payslip'].browse(docids)
        employee_data = {}

        # Organize payslips by employee
        for payslip in docs:
            employee = payslip.employee_id
            if employee.id not in employee_data:
                employee_data[employee.id] = {
                    'employee': employee,
                    'payslips': []
                }
            employee_data[employee.id]['payslips'].append(payslip)

        # Prepare the data in a format that avoids duplication
        employee_data_list = list(employee_data.values())

        _logger.info(f'Employee data: {employee_data_list}')
        
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'employee_data': employee_data_list,
            'time': fields.Datetime.now(),
        }
    

class ReportPayslipEtat1(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.report_payslip_etat1'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.payslip'].browse(docids)
        employee_data = {}
        salary_rules = {}

        # Organize payslips by employee and collect salary rules
        for payslip in docs:
            employee = payslip.employee_id
            if employee.id not in employee_data:
                employee_data[employee.id] = {
                    'employee': employee,
                    'payslips': []
                }
            employee_data[employee.id]['payslips'].append(payslip)

            categories = ['BASIC', 'ALW', 'HPS']

            for line in payslip.line_ids:
                if line.category_id.code in categories and line.code not in salary_rules:
                    salary_rules[line.code] = line.code.replace('BASIC', 'SLBASE').replace('SENIORITY', 'ANCIEN').replace('SURSAL','SURSA').replace('EXTRA_HOURS_', 'HS').replace('TECHPROD', 'T PROD').replace('RENDCOL', 'REND').replace('TRANSP', 'TRANS').replace('DIFF', 'DIFFER').replace('LOGEM', 'LOG').replace('TELEPH', 'TEL').replace('RESPONS', 'RESP').replace('ASTREINT', 'ASTR').replace('PFONC', 'FONC').replace('ELOIGNEM', 'ELOI').replace('TECHNICIT3', 'P TECH').replace('INTERIM', 'P INTER').replace('CHARGELOC', 'CC LOG').replace('CAISSE','P CAISSE')
                    
        # Prepare the data in a format that avoids duplication
        employee_data_list = list(employee_data.values())
        
        start_date = docs[0].payslip_run_id.date_start
        end_date = docs[0].payslip_run_id.date_end

        employee_data_list = list(employee_data.values())

        # ➤ Définir les codes à afficher en priorité (dans l'ordre souhaité)
        priority_codes = [
            'SLBASE', 'ANCIEN', 'SURSA', 'HS115', 'HS140', 'HS150', 'HS200', 'P TECH', 'REND', 'TRANS', 'DIFFER',
            'LOG', 'TEL', 'PUV', 'RESP', 'ASTR', 'FONC', 'SAISI', 'RISQ', 'ELOI', 'CC LOG', 'PCAIS',
            'P TECH', 'P INTER'
        ]

        # ➤ Fonction de tri personnalisée
        def sort_key(item):
            code_label = item[1]  # Ex: 'SLBASE', 'RESP', etc.
            if code_label in priority_codes:
                return (0, priority_codes.index(code_label))
            return (1, code_label)

        # ➤ Tri du dictionnaire selon l’ordre personnalisé
        sorted_salary_rules = dict(sorted(salary_rules.items(), key=sort_key))

        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'employee_data': employee_data_list,
            'salary_rules': sorted_salary_rules,
            'time': fields.Datetime.now(),
            'start_date': start_date,
            'end_date': end_date,
        }

    
class ReportPayslipEtat2(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.report_payslip_etat2'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Fetch payslips based on the provided docids
        docs = self.env['hr.payslip'].browse(docids)
        employee_data = {}
        salary_rules = {}

        # Organize payslips by employee
        for payslip in docs:
            employee = payslip.employee_id
            if employee.id not in employee_data:
                employee_data[employee.id] = {
                    'employee': employee,
                    'payslips': []
                }
            employee_data[employee.id]['payslips'].append(payslip)

            categories = ['GROSS', 'DED' , 'CNSS', 'CNAM', 'ITS', 'CG', 'AVS_ACPT', 'PRET', 'AVS_ACPT', 'AUTREALW']
            for line in payslip.line_ids:
                if line.category_id.code in categories and line.code not in salary_rules:
                    label = line.code.replace('GROSS', 'BRUT').replace('CNAM_ALLOCG', 'CNAM CG').replace('CNSS_ALLOCG', 'CNSS CG').replace('ITS_ALLOCG', 'ITS CG').replace('ALLOCG', 'BRUT CG')
                    rule_obj = self.env['hr.salary.rule'].search([('code', '=', line.code)], limit=1)
                    salary_rules[line.code] = {
                        'label': label,
                        'position': rule_obj.category_id.position if rule_obj and rule_obj.category_id else 9999
                    }
        # Prepare the data in a format that avoids duplication
        employee_data_list = list(employee_data.values()) 

        start_date = docs[0].payslip_run_id.date_start
        end_date = docs[0].payslip_run_id.date_end

        _logger.info(f'Employee data: {employee_data_list}')
        
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'employee_data': employee_data_list,
            'salary_rules': salary_rules,
            'time': fields.Datetime.now(),
            'start_date': start_date,
            'end_date': end_date,
        }
    
    
class ReportPayslipCtr(models.AbstractModel):
    _name = 'report.l10n_mr_hr_payroll.report_payslip_journal_control'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Define the month and year for filtering
        month = 5  # May
        year = fields.Date.today().year

        # Fetch payslips based on the provided docids and filter by month and year
        docs = self.env['hr.payslip'].browse(docids).filtered(lambda p: p.date_to.month == month and p.date_to.year == year)
        employee_data = {}

        # Organize payslips by employee
        for payslip in docs:
            if payslip.state == 'paid':  # Only consider paid payslips
                for line in payslip.line_ids:
                    rule = line.salary_rule_id
                    account_debit = rule.account_debit
                    account_credit = rule.account_credit

                    key = (rule.name, account_debit or account_credit)

                    if key not in employee_data:
                        employee_data[key] = {
                            'rule_name': rule.name,
                            'account_code': (account_debit or account_credit).code if account_debit or account_credit else 'N/A',
                            'account_name': (account_debit or account_credit).name if account_debit or account_credit else 'N/A',
                            'debit': 0.0,
                            'credit': 0.0,
                        }

                    employee_data[key]['debit'] += line.total if account_debit else 0.0
                    employee_data[key]['credit'] += line.total if account_credit else 0.0

        # Convert dictionary to list for easy access in the template
        employee_data_list = list(employee_data.values())

        _logger.info(f'Employee data with payslip lines: {employee_data_list}')

        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip',
            'employee_data': employee_data_list,
            'time': fields.Datetime.now(),
        }


# class ReportPayslipEtat2(models.AbstractModel):
#     _name = 'report.l10n_mr_hr_payroll.action_report_payslip_journal_ctr'

#     @api.model
#     def _get_report_values(self, docids, data=None):
#         docs = self.env['hr.payslip'].browse(docids)
#         employee_data = {}

#         for payslip in docs:
#             if payslip.state == 'paid':  # Check if the payslip is in 'paid' state

#                 employee = payslip.employee_id
#                 if employee.id not in employee_data:
#                     employee_data[employee.id] = {
#                         'employee': employee,
#                         'payslips': []
#                     }
#                 employee_data[employee.id]['payslips'].append(payslip)

#             employee_data_list = list(employee_data.values())

#         _logger.info(f'Employee data: {employee_data_list}')
        
#         return {
#             'doc_ids': docids,
#             'doc_model': 'hr.payslip',
#             'employee_data': employee_data_list,
#             'time': fields.Datetime.now(),
#         }