from odoo import models, fields, api, _


class BankTransferBatch(models.Model):
    _name = 'bank.transfer.batch'
    _description = 'Lot de virement bancaire'
    _order = 'date desc, name desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Nom du lot',
        required=True,
        default=lambda self: self._default_name(),
        tracking=True
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        tracking=True
    )
    
    state = fields.Selection([
        ('a_draft', 'Brouillon'),
        ('b_confirmed', 'Confirmé'),
        ('c_done', 'Traité'),
    ], string='État', default='a_draft', required=True, tracking=True)
    
    transfer_ids = fields.One2many(
        'bank.transfer',
        'batch_id',
        string='Virements'
    )
    
    transfer_count = fields.Integer(
        string='Nombre de virements',
        compute='_compute_transfer_count',
        store=True
    )
    
    total_amount = fields.Monetary(
        string='Montant total',
        compute='_compute_total_amount',
        store=True,
        currency_field='currency_id'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    notes = fields.Text(string='Notes')
    
    color = fields.Integer(string='Color Index')

    @api.model
    def _default_name(self):
        """Génère un nom par défaut pour le lot"""
        return self.env['ir.sequence'].next_by_code('bank.transfer.batch') or 'Nouveau lot'

    @api.depends('transfer_ids')
    def _compute_transfer_count(self):
        """Calcule le nombre de virements dans le lot"""
        for record in self:
            record.transfer_count = len(record.transfer_ids)

    @api.depends('transfer_ids', 'transfer_ids.salaire_corrige', 'transfer_ids.salaire')
    def _compute_total_amount(self):
        """Calcule le montant total du lot"""
        for record in self:
            total = 0.0
            for transfer in record.transfer_ids:
                # Utiliser salaire_corrige s'il existe, sinon salaire
                total += transfer.salaire_corrige or transfer.salaire or 0.0
            record.total_amount = total

    def action_confirm(self):
        """Confirme le lot"""
        for record in self:
            record.write({'state': 'b_confirmed'})
            record.message_post(
                body=_('Le lot de virement a été confirmé.'),
                subject=_('Lot confirmé')
            )

    def action_c_done(self):
        """Marque le lot comme traité"""
        for record in self:
            record.write({'state': 'c_done'})
            record.message_post(
                body=_('Le lot de virement a été traité avec succès. Total: %s virements pour un montant de %s %s.') % (
                    record.transfer_count,
                    record.total_amount,
                    record.currency_id.symbol
                ),
                subject=_('Lot traité')
            )

    def action_a_draft(self):
        """Remet le lot en brouillon"""
        for record in self:
            record.write({'state': 'a_draft'})
            record.message_post(
                body=_('Le lot de virement a été remis en brouillon.'),
                subject=_('Lot remis en brouillon')
            )

    def action_open_transfers(self):
        """Ouvre la vue des virements du lot avec toutes les vues disponibles"""
        self.ensure_one()
        return {
            'name': f'Virements du lot: {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'bank.transfer',
            'view_mode': 'list,kanban,form,pivot,graph,calendar',
            'domain': [('batch_id', '=', self.id)],
            'context': {
                'default_batch_id': self.id,
                'active_batch_id': self.id,
            },
        }

    def action_regenerate_all_lines(self):
        """Régénère les lignes de répartition pour tous les virements du lot"""
        for transfer in self.transfer_ids:
            transfer._generate_transfer_lines()
        
        total_lines = sum(len(t.transfer_line_ids) for t in self.transfer_ids)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Répartitions régénérées'),
                'message': _('%s ligne(s) de répartition créée(s) pour %s virement(s).') % (
                    total_lines,
                    len(self.transfer_ids)
                ),
                'type': 'success',
            }
        }

    @api.model
    def create_batch_from_versions(self, name, date, version_ids):
        """
        Crée un lot de virement bancaire avec les versions (hr.version) sélectionnées
        
        :param name: Nom du lot
        :param date: Date du lot
        :param version_ids: Liste des IDs de hr.version sélectionnés
        :return: Dict avec l'ID du lot créé
        """
        # Créer le lot
        batch = self.create({
            'name': name,
            'date': date,
        })
        
        # Récupérer les versions
        versions = self.env['hr.version'].browse(version_ids)
        
        # Créer les virements pour chaque version (employé)
        transfers_created = []
        employee_names = []
        for version in versions:
            if version.employee_id:
                transfer = self.env['bank.transfer'].create({
                    'batch_id': batch.id,
                    'employee_id': version.employee_id.id,
                })
                transfers_created.append(transfer)
                employee_names.append(version.employee_id.name)
        
        # Ajouter un message dans le chatter
        batch.message_post(
            body=_('Lot créé avec succès. %s virement(s) ajouté(s) pour les employés suivants : %s') % (
                len(transfers_created),
                ', '.join(employee_names)
            ),
            subject=_('Lot créé depuis hr.version')
        )
        
        return {
            'batch_id': batch.id,
            'transfer_count': len(transfers_created),
        }

