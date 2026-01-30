# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError

from lxml import etree


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    def _paie_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_paie")

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
            raise AccessError(_("Vous n'êtes pas autorisé à créer des bulletins de paie."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des bulletins de paie."))
        return super().write(vals)

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des bulletins de paie."))
        if self._paie_no_delete():
            raise AccessError(_("Le groupe PAIE n'est pas autorisé à supprimer des bulletins de paie."))
        return super().unlink()


class HrPayslipLine(models.Model):
    _inherit = "hr.payslip.line"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    def _paie_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_paie")

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
            raise AccessError(_("Vous n'êtes pas autorisé à créer des lignes de paie."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des lignes de paie."))
        return super().write(vals)

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des lignes de paie."))
        if self._paie_no_delete():
            raise AccessError(_("Le groupe PAIE n'est pas autorisé à supprimer des lignes de paie."))
        return super().unlink()


class HrPayslipRun(models.Model):
    _inherit = "hr.payslip.run"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    def _paie_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_paie")

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
            raise AccessError(_("Vous n'êtes pas autorisé à créer des lots de paie."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des lots de paie."))
        return super().write(vals)

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des lots de paie."))
        if self._paie_no_delete():
            raise AccessError(_("Le groupe PAIE n'est pas autorisé à supprimer des lots de paie."))
        return super().unlink()
