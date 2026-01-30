# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError

from lxml import etree


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)

        if (self._dg_read_all_active() or self._siha_agent_read_only() or self._finance_read_only()) and view_type in {"list", "kanban", "form"}:
            node = etree.fromstring(result["arch"])
            node.set("create", "0")
            node.set("edit", "0")
            node.set("delete", "0")
            result["arch"] = etree.tostring(node, encoding="unicode")

        return result

    def _bd_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_bd_manager")

    def _siha_agent_read_only(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_siha_agent")

    def _finance_read_only(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_finance")

    @api.model_create_multi
    def create(self, vals_list):
        if self._dg_read_all_active() or self._siha_agent_read_only() or self._finance_read_only():
            raise AccessError(_("Vous n'êtes pas autorisé à créer des opportunités/pistes CRM."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active() or self._siha_agent_read_only() or self._finance_read_only():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des opportunités/pistes CRM."))
        return super().write(vals)

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des opportunités/pistes CRM."))
        if self._siha_agent_read_only():
            raise AccessError(_("Le groupe SIHA AGENT n'est pas autorisé à supprimer des leads/opportunités."))
        if self._finance_read_only():
            raise AccessError(_("Le groupe FINANCE n'est pas autorisé à supprimer des leads/opportunités."))
        if self._bd_manager_no_delete():
            raise AccessError(_("Le groupe BD MANAGER n'est pas autorisé à supprimer des leads/opportunités."))
        return super().unlink()
