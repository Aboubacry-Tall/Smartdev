from odoo import models, fields, api

class ReportJournalBank(models.AbstractModel):
    _name = 'report.smart_payroll.bank_journal_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.payslip'].browse(docids)

        bank = docs[0].employee_id.bank_account_id.acc_number
        date_from = docs[0].date_from
        date_to = docs[0].date_to
        
        return {
            'doc_ids': docids,
            'docs': docs,
            'doc_model': 'hr.payslip',
            'time': fields.Datetime.now(),
            'bank': bank,
            'date_from': date_from,
            'date_to': date_to,
        }

class ReportJournalControl(models.AbstractModel):
    _name = 'report.smart_payroll.control_journal_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.payslip'].browse(docids)

        date_from = docs[0].date_from
        date_to = docs[0].date_to
        
        return {
            'doc_ids': docids,
            'docs': docs,
            'doc_model': 'hr.payslip',
            'time': fields.Datetime.now(),
            'date_from': date_from,
            'date_to': date_to,
        }