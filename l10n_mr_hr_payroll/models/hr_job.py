
from odoo import fields, models
   
    
class HrJob(models.Model):
    _inherit = 'hr.job'

    p_prime_caisse = fields.Float(string="Prime de caisse", tracking=True)
    p_fonction = fields.Float(string="Prime de fonction", tracking=True)
    p_caution = fields.Float(string="Prime/caution", tracking=True)
    p_charge_locative = fields.Float(string="Charge locative", tracking=True)
    
    p_transport = fields.Float(string="Transport", required=True, tracking=True)
    p_telephone = fields.Float(string="Prime de telephone", required=True, tracking=True)
    p_logt = fields.Float(string="Prime de logment", required=True, tracking=True)
    p_eau_electricite = fields.Float(string="Eau et elect", required=True, tracking=True)
    l10n_mr_Astreinte = fields.Float(string="Astreinte", tracking=True)
    l10n_mr_lait = fields.Boolean(string="Prime de LAIT", tracking=True)




