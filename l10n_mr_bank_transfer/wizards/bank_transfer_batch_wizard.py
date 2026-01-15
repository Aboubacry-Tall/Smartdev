from odoo import models, fields, api, _


class BankTransferBatchWizardStep1(models.TransientModel):
    _name = 'bank.transfer.batch.wizard.step1'
    _description = 'Assistant de création de lot - Étape 1'

    name = fields.Char(
        string='Nom du lot',
        required=True,
        default=lambda self: self._default_name()
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today
    )

    @api.model
    def _default_name(self):
        """Génère un nom par défaut pour le lot"""
        return self.env['ir.sequence'].next_by_code('bank.transfer.batch') or ''

    def action_next(self):
        """Ouvre la liste de sélection des versions (employés)"""
        self.ensure_one()
        return {
            'name': _('Sélectionnez les employés '),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.version',
            'view_mode': 'list',
            'view_id': self.env.ref('l10n_mr_bank_transfer.view_hr_version_bank_transfer_selection_list').id,
            'domain': [('active', '=', True)],
            'target': 'new',
            'context': {
                'default_batch_name': self.name,
                'default_batch_date': self.date,
                'dialog_size': 'extra-large',
            },
        }


class BankTransferBatchWizardEmployeeLine(models.TransientModel):
    """Ligne d'employé pour la sélection dans le wizard"""
    _name = 'bank.transfer.batch.wizard.employee.line'
    _description = 'Ligne employé du wizard'
    _order = 'employee_name'

    wizard_id = fields.Many2one(
        'bank.transfer.batch.wizard.step2',
        string='Wizard',
        required=True,
        ondelete='cascade'
    )
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        required=True,
        readonly=True
    )
    
    employee_name = fields.Char(
        string='Nom',
        related='employee_id.name',
        readonly=True
    )
    
    matricule = fields.Char(
        string='Matricule',
        related='employee_id.matricule',
        readonly=True
    )
    
    version_id = fields.Many2one(
        'hr.version',
        string='Contrat',
        readonly=True
    )
    
    job_title = fields.Char(
        string='Poste',
        related='employee_id.job_title',
        readonly=True
    )
    
    selected = fields.Boolean(
        string='Sélectionner',
        default=True,
        help='Cocher pour inclure cet employé dans le lot'
    )


class BankTransferBatchWizardStep2(models.TransientModel):
    _name = 'bank.transfer.batch.wizard.step2'
    _description = 'Assistant de création de lot - Étape 2'

    name = fields.Char(
        string='Nom du lot',
        required=True,
        readonly=True
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        readonly=True
    )
    
    employee_line_ids = fields.One2many(
        'bank.transfer.batch.wizard.employee.line',
        'wizard_id',
        string='Employés disponibles'
    )
    
    employee_count = fields.Integer(
        string='Nombre d\'employés sélectionnés',
        compute='_compute_employee_count'
    )

    @api.depends('employee_line_ids', 'employee_line_ids.selected')
    def _compute_employee_count(self):
        """Calcule le nombre d'employés sélectionnés"""
        for record in self:
            record.employee_count = len(record.employee_line_ids.filtered('selected'))

    @api.model
    def default_get(self, fields_list):
        """Récupère les valeurs de l'étape 1 et charge les employés disponibles"""
        res = super().default_get(fields_list)
        
        # Récupérer les valeurs de l'étape 1
        if 'name' in self.env.context:
            res['name'] = self.env.context.get('default_name')
        if 'date' in self.env.context:
            res['date'] = self.env.context.get('default_date')
        
        # Charger les employés avec contrat actif
        if 'employee_line_ids' in fields_list:
            employee_lines = []
            
            # Rechercher tous les contrats actifs (hr.version)
            active_versions = self.env['hr.version'].search([
                ('active', '=', True),
            ])
            
            # Créer une ligne pour chaque employé avec contrat actif
            for version in active_versions:
                if version.employee_id:
                    employee_lines.append((0, 0, {
                        'employee_id': version.employee_id.id,
                        'version_id': version.id,
                        'selected': True,  # Tous cochés par défaut
                    }))
            
            res['employee_line_ids'] = employee_lines
        
        return res


    def action_create_batch(self):
        """Crée le lot et les virements associés"""
        self.ensure_one()
        
        # Récupérer les lignes d'employés sélectionnées
        selected_lines = self.employee_line_ids.filtered('selected')
        
        if not selected_lines:
            # Si aucun employé n'est sélectionné, afficher un message d'erreur
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Erreur'),
                    'message': _('Veuillez sélectionner au moins un employé.'),
                    'type': 'danger',
                    'sticky': False,
                }
            }
        
        # Créer le lot
        batch = self.env['bank.transfer.batch'].create({
            'name': self.name,
            'date': self.date,
        })
        
        # Créer les virements pour chaque employé sélectionné
        transfers_created = []
        employee_names = []
        for line in selected_lines:
            transfer = self.env['bank.transfer'].create({
                'batch_id': batch.id,
                'employee_id': line.employee_id.id,
            })
            transfers_created.append(transfer)
            employee_names.append(line.employee_id.name)
        
        # Ajouter un message dans le chatter du lot
        batch.message_post(
            body=_('Lot créé avec succès. %s virement(s) ajouté(s) pour les employés suivants : %s') % (
                len(transfers_created),
                ', '.join(employee_names)
            ),
            subject=_('Lot créé')
        )
        
        # Retourner l'action pour ouvrir le lot créé
        return {
            'name': _('Lot de virement bancaire'),
            'type': 'ir.actions.act_window',
            'res_model': 'bank.transfer.batch',
            'res_id': batch.id,
            'view_mode': 'form',
            'target': 'current',
        }
