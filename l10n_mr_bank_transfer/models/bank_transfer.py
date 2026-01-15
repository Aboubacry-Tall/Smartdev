from odoo import models, fields, api, _

try:
    import qrcode
    import base64
    from io import BytesIO
except Exception:  # pragma: no cover
    qrcode = None
    base64 = None
    BytesIO = None


class BankTransfer(models.Model):
    _name = 'bank.transfer'
    _description = 'Journal de virement bancaire'
    _order = 'matricule'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_batch_id(self):
        """Récupère le batch_id depuis le contexte"""
        return self.env.context.get('default_batch_id', False)

    batch_id = fields.Many2one(
        'bank.transfer.batch',
        string='Lot',
        required=True,
        ondelete='cascade',
        index=True,
        default=_get_default_batch_id
    )
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        required=True,
        ondelete='cascade'
    )
    
    # Champs related depuis hr.employee
    matricule = fields.Char(
        string='Matricule',
        related='employee_id.matricule',
        readonly=True,
        store=True
    )
    
    name = fields.Char(
        string='Nom',
        related='employee_id.name',
        readonly=True,
        store=True
    )
    
    job_title = fields.Char(
        string='Poste',
        related='employee_id.job_title',
        readonly=True,
        store=True
    )
    
    department_id = fields.Many2one(
        'hr.department',
        string='Département',
        related='employee_id.department_id',
        readonly=True,
        store=True
    )
    
    # Lignes de virement par compte bancaire
    transfer_line_ids = fields.One2many(
        'bank.transfer.line',
        'transfer_id',
        string='Répartition par compte'
    )

    exchange_rate_date_mismatch = fields.Boolean(
        string="Décalage taux de change",
        compute="_compute_exchange_rate_date_mismatch",
        store=False,
        readonly=True,
        help="Vrai si au moins une ligne utilise un taux (date virement) différent du dernier taux disponible.",
    )
    
    # Champs related depuis les comptes bancaires
    bank_account_ids = fields.Many2many(
        'res.partner.bank',
        string='Comptes bancaires',
        compute='_compute_bank_account_ids',
        readonly=True
    )
    
    bank_account_id = fields.Many2one(
        'res.partner.bank',
        string='Compte bancaire principal',
        compute='_compute_bank_account',
        store=True
    )
    
    banques = fields.Char(
        string='Banques',
        compute='_compute_bank_info',
        store=True
    )
    
    code_banque = fields.Char(
        string='Code banque',
        compute='_compute_bank_info',
        store=True
    )
    
    bank_country_id = fields.Many2one(
        'res.country',
        string='Pays de la banque',
        compute='_compute_bank_info',
        store=True
    )
    
    # Champs salaires
    salaire = fields.Monetary(
        string='Salaire (Net à payer)',
        currency_field='currency_id',
        help='Salaire net à payer provenant du fichier Excel'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        related='batch_id.currency_id',
        readonly=True,
        store=True,
    )

    source_currency_id = fields.Many2one(
        'res.currency',
        string='Devise source',
        related='batch_id.source_currency_id',
        readonly=False,
        store=True,
    )

    date = fields.Date(
        string='Date',
        related='batch_id.date',
        readonly=True,
        store=True,
    )

    def _default_transfer_type(self):
        batch_id = self.env.context.get('default_batch_id') or self.env.context.get('active_batch_id')
        if batch_id:
            batch = self.env['bank.transfer.batch'].browse(batch_id)
            if batch.exists() and batch.transfer_type:
                return batch.transfer_type
        return 'simple'

    transfer_type = fields.Selection(
        [
            ('simple', 'Virement Simple'),
            ('transfer', 'Transfert (International)'),
        ],
        string='Type de virement',
        default=_default_transfer_type,
        tracking=True,
        required=True,
    )

    source_account_id = fields.Many2one(
        'res.partner.bank',
        string='Compte source',
        related='batch_id.source_account_id',
        readonly=True,
        store=True,
    )

    description = fields.Text(
        string='Motif',
        related='batch_id.description',
        readonly=True,
        store=True,
    )

    order_reference = fields.Char(
        string='Référence ordre',
        compute='_compute_order_reference',
        store=True,
        readonly=True,
    )
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('done', 'Payé'),
        ('cancel', 'Annulé'),
    ], string='État', default='draft', required=True, tracking=True)

    @api.depends('batch_id.name', 'matricule')
    def _compute_order_reference(self):
        for record in self:
            if record.batch_id and record.batch_id.name and record.matricule:
                record.order_reference = f"{record.batch_id.name}-{record.matricule}"
            elif record.batch_id and record.batch_id.name:
                record.order_reference = record.batch_id.name
            else:
                record.order_reference = str(record.id) if record.id else ''

    def get_qr_code(self):
        """QR code base64 (PNG) basé sur la référence de l'ordre."""
        self.ensure_one()
        if not qrcode or not base64 or not BytesIO:
            return False
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.order_reference or self.display_name or '')
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()

    def get_lines_grouped_by_bank(self):
        """Retourne les lignes de virement groupées par banque pour le rapport"""
        self.ensure_one()
        grouped = {}
        for line in self.transfer_line_ids:
            bank_id = line.bank_id.id if line.bank_id else 0
            bank_name = line.bank_id.name if line.bank_id else 'Sans banque'
            if bank_id not in grouped:
                grouped[bank_id] = {
                    'bank_id': line.bank_id,
                    'bank_name': bank_name,
                    'lines': self.env['bank.transfer.line']
                }
            grouped[bank_id]['lines'] |= line
        
        # Si aucune ligne, retourner un groupe vide
        if not grouped:
            grouped[0] = {
                'bank_id': False,
                'bank_name': '',
                'lines': self.env['bank.transfer.line']
            }
        
        # Convertir en liste pour le template
        return list(grouped.values())

    def action_print_order(self):
        """Imprime l'ordre de virement selon le type sélectionné sur le lot."""
        self.ensure_one()
        if self.transfer_type == 'simple':
            return self.env.ref('l10n_mr_bank_transfer.action_report_bank_transfer_order_simple').report_action(self)
        # transfer (international) / fallback
        return self.env.ref('l10n_mr_bank_transfer.action_report_bank_transfer_order_internal').report_action(self)

    @api.depends('employee_id', 'employee_id.bank_account_ids')
    def _compute_bank_account_ids(self):
        """Récupère les comptes bancaires de l'employé"""
        for record in self:
            if record.employee_id and record.employee_id.bank_account_ids:
                record.bank_account_ids = [(6, 0, record.employee_id.bank_account_ids.ids)]
            else:
                record.bank_account_ids = [(5, 0, 0)]

    @api.depends('transfer_line_ids.exchange_rate_date_mismatch')
    def _compute_exchange_rate_date_mismatch(self):
        for record in self:
            record.exchange_rate_date_mismatch = any(record.transfer_line_ids.mapped('exchange_rate_date_mismatch'))

    @api.depends('employee_id', 'employee_id.bank_account_ids')
    def _compute_bank_account(self):
        """Calcule le compte bancaire principal de l'employé"""
        for record in self:
            if record.employee_id:
                # Utiliser primary_bank_account_id s'il existe, sinon le premier compte
                record.bank_account_id = (
                    record.employee_id.primary_bank_account_id or
                    record.employee_id.bank_account_ids[:1] if record.employee_id.bank_account_ids else False
                )
            else:
                record.bank_account_id = False

    @api.depends('bank_account_id')
    def _compute_bank_info(self):
        """Calcule les informations bancaires depuis le compte bancaire principal"""
        for record in self:
            if record.bank_account_id:
                record.banques = record.bank_account_id.bank_id.name if record.bank_account_id.bank_id else ''
                record.code_banque = record.bank_account_id.bank_bic or ''
                record.bank_country_id = record.bank_account_id.bank_id.country if record.bank_account_id.bank_id else False
            else:
                record.banques = ''
                record.code_banque = ''
                record.bank_country_id = False

    def action_return_to_batch(self):
        """Retourne à la vue du lot"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'bank.transfer.batch',
            'res_id': self.batch_id.id,
            'views': [[False, 'form']],
            'target': 'current',
        }

    def action_export_excel(self):
        """Exporte les virements vers Excel"""
        # Cette méthode sera appelée depuis le JavaScript
        # Pour l'instant, on retourne juste un message
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Export Excel',
                'message': 'Fonctionnalité à implémenter',
                'type': 'info',
            }
        }

    def action_import_salaries(self):
        """Ouvre le wizard d'import des salaires"""
        self.ensure_one()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Import',
                'message': 'Wizard d\'import à créer',
                'type': 'info',
            }
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Crée le virement et génère automatiquement les lignes de répartition"""
        # Si le type n'est pas explicitement fourni, l'hériter du lot.
        for vals in vals_list:
            if not vals.get('transfer_type') and vals.get('batch_id'):
                batch = self.env['bank.transfer.batch'].browse(vals['batch_id'])
                if batch.exists() and batch.transfer_type:
                    vals['transfer_type'] = batch.transfer_type
        records = super().create(vals_list)
        for record in records:
            record._generate_transfer_lines()
        return records

    def _generate_transfer_lines(self):
        """Génère automatiquement les lignes de répartition par compte bancaire"""
        self.ensure_one()
        
        # Supprimer les lignes existantes si on régénère
        self.transfer_line_ids.unlink()
        
        # Récupérer le salaire à répartir
        salaire_a_repartir = self.salaire
        
        # Si pas de salaire défini, essayer de récupérer depuis hr.version
        if not salaire_a_repartir and self.employee_id:
            # Chercher le contrat actif (hr.version) de l'employé
            version = self.env['hr.version'].search([
                ('employee_id', '=', self.employee_id.id),
                ('active', '=', True),
            ], limit=1)
            if version and version.wage:
                salaire_a_repartir = version.wage
                # Mettre à jour le champ salaire
                self.salaire = salaire_a_repartir
        
        if not salaire_a_repartir or not self.employee_id:
            return
        
        # Utiliser la distribution salariale standard d'Odoo (salary_distribution)
        salary_distribution = self.employee_id.salary_distribution or {}
        
        if not salary_distribution:
            # Si pas de distribution, mettre tout sur le compte principal
            bank_accounts = self.employee_id.bank_account_ids
            compte_principal = self.bank_account_id or (bank_accounts[0] if bank_accounts else None)
            if compte_principal:
                self.env['bank.transfer.line'].create({
                    'transfer_id': self.id,
                    'bank_account_id': compte_principal.id,
                    'amount': salaire_a_repartir,
                    'sequence': 10,
                })
            return
        
        import logging
        _logger = logging.getLogger(__name__)
        
        # Collecter les montants fixes et pourcentages depuis salary_distribution
        montants_fixes = {}
        pourcentages = {}
        total_fixe = 0.0
        
        for bank_id_str, config in salary_distribution.items():
            bank_id = int(bank_id_str)
            amount = config.get('amount', 0)
            is_percentage = config.get('amount_is_percentage', False)
            
            if amount > 0:
                if is_percentage:
                    pourcentages[bank_id] = amount
                    _logger.info(f"Compte {bank_id}: pourcentage={amount}%")
                else:
                    montants_fixes[bank_id] = amount
                    total_fixe += amount
                    _logger.info(f"Compte {bank_id}: montant fixe={amount}")
        
        _logger.info(f"Salaire total: {salaire_a_repartir}")
        _logger.info(f"Total montants fixes: {total_fixe}")
        _logger.info(f"Pourcentages: {pourcentages}")
        
        # Créer les lignes de répartition
        lines_to_create = []
        sequence = 10
        
        # Étape 1 : Allouer les montants FIXES
        for account_id, montant_fixe in montants_fixes.items():
            lines_to_create.append({
                'transfer_id': self.id,
                'bank_account_id': account_id,
                'amount': montant_fixe,
                'sequence': sequence,
            })
            sequence += 10
            _logger.info(f"Ligne fixe: compte {account_id} = {montant_fixe}")
        
        # Calculer le reste après les montants fixes
        reste_apres_fixes = salaire_a_repartir - total_fixe
        _logger.info(f"Reste après fixes: {reste_apres_fixes}")
        
        # Étape 2 : Allouer les POURCENTAGES sur le RESTE
        if pourcentages and reste_apres_fixes > 0:
            for account_id, pourcent in pourcentages.items():
                montant = reste_apres_fixes * (pourcent / 100.0)
                lines_to_create.append({
                    'transfer_id': self.id,
                    'bank_account_id': account_id,
                    'amount': montant,
                    'sequence': sequence,
                })
                sequence += 10
                _logger.info(f"Ligne pourcentage: compte {account_id} = {pourcent}% de {reste_apres_fixes} = {montant}")
        
        # Créer les lignes
        if lines_to_create:
            total_distribue = sum(line['amount'] for line in lines_to_create)
            _logger.info(f"Total distribué: {total_distribue} (salaire: {salaire_a_repartir})")
            self.env['bank.transfer.line'].create(lines_to_create)

    def action_regenerate_lines(self):
        """Régénère les lignes de répartition (comme compute_sheet dans les fiches de paie)"""
        for record in self:
            record._generate_transfer_lines()
        
        # Retourner True pour recharger automatiquement la vue (comme compute_sheet)
        return True
    
    def action_set_to_draft(self):
        """Remettre à l'état brouillon"""
        self.write({'state': 'draft'})
    
    def action_mark_as_paid(self):
        """Marquer comme payé"""
        self.write({'state': 'done'})
    
    def action_cancel(self):
        """Annuler le virement"""
        self.write({'state': 'cancel'})
    
    def action_print_report_pdf(self):
        """Imprimer le rapport groupé par banque avec sous-totaux"""
        # Récupérer le filtre de banque si l'utilisateur a sélectionné une banque
        bank_filter = self._get_bank_filter()
        
        # Retourner l'action de rapport avec le contexte
        return self.env.ref('l10n_mr_bank_transfer.action_report_bank_transfer_grouped').with_context(
            bank_filter=bank_filter
        ).report_action(self)
    
    def _get_bank_filter(self):
        """Récupère le filtre de banque depuis le contexte ou détermine la banque commune"""
        # Si un seul virement et filtré par banque dans le search
        if self.env.context.get('search_default_group_by_banque'):
            # Récupérer toutes les banques distinctes
            banks = self.mapped('banques')
            if len(set(banks)) == 1:
                return banks[0] if banks[0] else None
        
        # Sinon, vérifier si tous les virements sont de la même banque
        banks = self.mapped('banques')
        if banks and len(set(banks)) == 1:
            return banks[0]
        
        return None
    
    def action_export_report_excel(self):
        """Exporter le rapport de répartition en Excel (filtré par banque si nécessaire)"""
        import xlsxwriter
        from io import BytesIO
        import base64
        
        # Récupérer le filtre de banque
        bank_filter = self._get_bank_filter()
        
        # Créer un fichier Excel en mémoire
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Répartition des virements')
        
        # Formats avec couleurs vives et modernes
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D6EAF8',
            'font_color': '#212529',
            'border': 1,
            'border_color': '#CED4DA',
            'align': 'center',
            'valign': 'vcenter'
        })
        
        cell_format = workbook.add_format({
            'border': 1,
            'border_color': '#CED4DA',
            'font_color': '#212529',
            'align': 'left',
            'valign': 'vcenter'
        })
        
        money_format = workbook.add_format({
            'border': 1,
            'border_color': '#CED4DA',
            'font_color': '#212529',
            'align': 'right',
            'valign': 'vcenter',
            'num_format': '#,##0.00'
        })
        
        # Titre principal
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#4A90E2',
            'font_color': 'white'
        })
        
        start_row = 0
        if bank_filter:
            worksheet.merge_range('A1:E1', f'JOURNAL DE BANQUE - {bank_filter}', title_format)
        else:
            worksheet.merge_range('A1:E1', 'RAPPORT DES VIREMENTS BANCAIRES - Groupé par banque', title_format)
        
        # Info du lot
        if self and self[0].batch_id:
            info_format = workbook.add_format({'italic': True, 'align': 'center'})
            batch_info = f"Lot: {self[0].batch_id.name} - Date: {self[0].batch_id.date}"
            worksheet.merge_range('A2:E2', batch_info, info_format)
            start_row = 3
        else:
            start_row = 2
        
        # Dimensions des colonnes
        worksheet.set_column('A:A', 12)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 15)
        
        # Collecter toutes les banques
        all_banks = set()
        for transfer in self:
            if transfer.transfer_line_ids:
                for line in transfer.transfer_line_ids:
                    if line.bank_id and (not bank_filter or line.bank_id.name == bank_filter):
                        all_banks.add(line.bank_id.name)
            elif not bank_filter or transfer.banques == bank_filter:
                if transfer.banques:
                    all_banks.add(transfer.banques)
        
        row = start_row
        all_subtotals = []
        
        # Format pour les en-têtes de banque
        bank_header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#4A90E2',
            'font_color': 'white',
            'border': 1,
            'border_color': '#CED4DA'
        })
        
        # Format pour les sous-totaux
        subtotal_format = workbook.add_format({
            'bold': True,
            'bg_color': '#E9ECEF',
            'font_color': '#212529',
            'border': 1,
            'border_color': '#CED4DA',
            'align': 'right',
            'num_format': '#,##0.00'
        })
        
        # Parcourir chaque banque
        for bank_name in sorted(all_banks):
            # En-tête de la banque
            worksheet.merge_range(row, 0, row, 4, f'🏦 {bank_name}', bank_header_format)
            row += 1
            
            # En-têtes des colonnes
            headers = ['Matricule', 'Nom et Prénom', 'Code BIC', 'N° Compte', 'Montant']
            column_header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D6EAF8',
                'font_color': '#212529',
                'border': 1,
                'border_color': '#CED4DA',
                'align': 'center'
            })
            for col, header in enumerate(headers):
                worksheet.write(row, col, header, column_header_format)
            row += 1
            
            # Données pour cette banque
            bank_total = 0.0
            
            for transfer in self:
                if transfer.transfer_line_ids:
                    # Filtrer les lignes de cette banque
                    filtered_lines = transfer.transfer_line_ids.filtered(lambda l: l.bank_id.name == bank_name)
                    for line in filtered_lines:
                        worksheet.write(row, 0, transfer.matricule or '', cell_format)
                        worksheet.write(row, 1, transfer.name or '', cell_format)
                        worksheet.write(row, 2, line.bank_bic or '', cell_format)
                        worksheet.write(row, 3, line.acc_number or '', cell_format)
                        worksheet.write(row, 4, line.amount, money_format)
                        bank_total += line.amount
                        row += 1
                elif transfer.banques == bank_name:
                    # Si pas de répartition et correspond à cette banque
                    worksheet.write(row, 0, transfer.matricule or '', cell_format)
                    worksheet.write(row, 1, transfer.name or '', cell_format)
                    worksheet.write(row, 2, transfer.code_banque or '', cell_format)
                    worksheet.write(row, 3, transfer.bank_account_id.acc_number if transfer.bank_account_id else '', cell_format)
                    worksheet.write(row, 4, transfer.salaire or 0, money_format)
                    bank_total += transfer.salaire or 0
                    row += 1
            
            # Sous-total de la banque
            worksheet.write(row, 0, '', subtotal_format)
            worksheet.write(row, 1, '', subtotal_format)
            worksheet.write(row, 2, '', subtotal_format)
            worksheet.write(row, 3, f'SOUS-TOTAL {bank_name}', subtotal_format)
            worksheet.write(row, 4, bank_total, subtotal_format)
            all_subtotals.append(bank_total)
            row += 2  # Espace après chaque banque
        
        # Total général (somme des sous-totaux)
        total_general_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4A90E2',
            'font_color': 'white',
            'border': 1,
            'border_color': '#CED4DA',
            'align': 'right',
            'font_size': 14,
            'num_format': '#,##0.00'
        })
        worksheet.write(row, 0, '', total_general_format)
        worksheet.write(row, 1, '', total_general_format)
        worksheet.write(row, 2, '', total_general_format)
        worksheet.write(row, 3, 'TOTAL GÉNÉRAL', total_general_format)
        worksheet.write(row, 4, sum(all_subtotals), total_general_format)
        
        workbook.close()
        output.seek(0)
        
        # Nom du fichier avec banque si filtrée
        filename = f'Journal_banque_{bank_filter}_{fields.Date.today()}.xlsx' if bank_filter else f'Répartition_virements_{fields.Date.today()}.xlsx'
        
        # Créer l'attachement
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        
        # Retourner l'action de téléchargement
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }


