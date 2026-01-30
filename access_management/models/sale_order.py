# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError

from lxml import etree


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)

        if self._dg_read_all_active() and view_type in {"list", "kanban", "form"}:
            node = etree.fromstring(result["arch"])
            # Hide UI actions
            node.set("create", "0")
            node.set("edit", "0")
            node.set("delete", "0")
            result["arch"] = etree.tostring(node, encoding="unicode")

        return result

    @api.model_create_multi
    def create(self, vals_list):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à créer des lignes de devis ou de commande."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des lignes de devis ou de commande."))
        return super().write(vals)

    def _bd_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_bd_manager")

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des lignes de devis ou de commande."))
        if self._bd_manager_no_delete():
            raise AccessError(_("Le groupe BD MANAGER n'est pas autorisé à supprimer des devis/commandes."))
        return super().unlink()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)

        if self._dg_read_all_active() and view_type in {"list", "kanban", "form"}:
            node = etree.fromstring(result["arch"])
            node.set("create", "0")
            node.set("edit", "0")
            node.set("delete", "0")
            result["arch"] = etree.tostring(node, encoding="unicode")

        return result

    @api.model_create_multi
    def create(self, vals_list):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à créer des lignes de devis ou de commande."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des lignes de devis ou de commande."))
        return super().write(vals)

    def _bd_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_bd_manager")

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des lignes de devis ou de commande."))
        if self._bd_manager_no_delete():
            raise AccessError(_("Le groupe BD MANAGER n'est pas autorisé à supprimer des lignes de devis/commande."))
        return super().unlink()

