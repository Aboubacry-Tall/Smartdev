# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _bd_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_bd_manager")

    def _siha_agent_read_only(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_siha_agent")

    def _finance_read_only(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_finance")

    @api.model_create_multi
    def create(self, vals_list):
        if self._siha_agent_read_only() or self._finance_read_only():
            raise AccessError(_("Vous n'êtes pas autorisé à créer des clients/contacts."))
        return super().create(vals_list)

    def write(self, vals):
        if self._siha_agent_read_only() or self._finance_read_only():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des clients/contacts."))
        return super().write(vals)

    def unlink(self):
        if self._siha_agent_read_only():
            raise AccessError(_("Le groupe SIHA AGENT n'est pas autorisé à supprimer des clients/contacts."))
        if self._finance_read_only():
            raise AccessError(_("Le groupe FINANCE n'est pas autorisé à supprimer des clients/contacts."))
        if self._bd_manager_no_delete():
            raise AccessError(_("Le groupe BD MANAGER n'est pas autorisé à supprimer des clients/contacts."))
        return super().unlink()
