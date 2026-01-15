from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Beneficiary(models.Model):
    _name = 'sogem.beneficiary'
    _description = 'Bénéficiaire des virements'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom', required=True, tracking=True)

    category = fields.Selection([
        ('employee', 'Salarié'),
        ('administrator', 'Administrateur'),
        ('supplier', 'Fournisseur'),
        ('study_office', "Bureau d'études"),
        ('work', 'Travaux'),
        ('partner', 'Partenaire'),
        ('other', 'Autre')
    ], string='Type de Bénéficiaire', required=True, tracking=True)
    
    category_id = fields.Many2one(
        'beneficiary.category', 
        string='Catégorie',
        help='Catégorie pour organiser les bénéficiaires'
    )

    country_id = fields.Many2one(
        'res.country', string='Pays', required=True, tracking=True)
    matricule = fields.Char(string='Matricule', required=True,
                            copy=False, index=True, unique=True, default="Nouveau")
    # ... autres champs du bénéficiaire ...

    address = fields.Char(string="Adresse")
    is_company_beneficiary = fields.Boolean(string='Bénéficiaire de l\'entreprise', default=False)

    partner_id = fields.Many2one(
        'res.partner',
        string='Partenaire',
        readonly=True,
        tracking=True,
        help='Partenaire créé automatiquement lors de la création du bénéficiaire'
    )

    bank_account_ids = fields.One2many(
        'sogem.bank.account', 'beneficiary_id', string="Comptes bancaires"
    )

    internal_number = fields.Char(
        string='Numéro interne', readonly=True, copy=False, tracking=True)

    active = fields.Boolean(default=True, tracking=True)

    locked = fields.Boolean(default=False, tracking=True)
    locked_reason = fields.Text(string='Raison du verrouillage', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        # Créer les partenaires avant de créer les bénéficiaires
        for vals in vals_list:
            # Générer le matricule automatiquement s'il n'est pas fourni
            if not vals.get('matricule'):
                vals['matricule'] = self.env['ir.sequence'].next_by_code(
                    'sogem.beneficiary.matricule') or 'NEW'
            
            if not vals.get('internal_number'):
                vals['internal_number'] = self.env['ir.sequence'].next_by_code(
                    'sogem.beneficiary')
            
            # Créer automatiquement un partenaire si non fourni
            if not vals.get('partner_id'):
                partner_vals = {
                    'name': vals.get('name', 'Nouveau partenaire'),
                    'country_id': vals.get('country_id', False),
                    'street': vals.get('address', False),
                    'is_company': False,  # Par défaut, on considère que c'est une personne
                }
                # Déterminer si c'est une entreprise selon la catégorie
                category = vals.get('category', '')
                if category in ('supplier', 'study_office', 'work', 'partner'):
                    partner_vals['is_company'] = True
                
                partner = self.env['res.partner'].create(partner_vals)
                vals['partner_id'] = partner.id
        
        return super().create(vals_list)

    

    def action_lock(self):
        self.ensure_one()
        return {
            'name': _('Verrouiller le bénéficiaire'),
            'type': 'ir.actions.act_window',
            'res_model': 'sogem.beneficiary.lock.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_beneficiary_id': self.id}
        }

    def action_unlock(self):
        self.ensure_one()
        self.write({
            'locked': False,
            'locked_reason': False
        })

    @api.model
    def name_search(self, name='', args=None, operator='=ilike', limit=100):
        """
        Override name_search to look up by 'matricule' or 'name'.
        Falls back to the default behavior if no name is specified.
        """
        args = args or []
        # If no search term, delegate to super
        if not name:
            return super().name_search(name, args, operator, limit)

        # Build a domain that searches either matricule or name
        domain = ['|', ('matricule', operator, name), ('name', operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()

    def name_get(self):
        result = []
        for rec in self:
            name = rec.name
            result.append((rec.id, name))
        return result


class BeneficiaryLockWizard(models.TransientModel):
    _name = 'sogem.beneficiary.lock.wizard'
    _description = 'Wizard de verrouillage des bénéficiaires'

    beneficiary_id = fields.Many2one(
        'sogem.beneficiary', string='Bénéficiaire', required=True)
    locked_reason = fields.Text(string='Raison du verrouillage', required=True)

    def action_lock(self):
        self.ensure_one()
        self.beneficiary_id.write({
            'locked': True,
            'locked_reason': self.locked_reason
        })
        return {'type': 'ir.actions.act_window_close'}
