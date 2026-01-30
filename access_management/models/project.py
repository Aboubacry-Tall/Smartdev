# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError

from lxml import etree


class ProjectProject(models.Model):
    _inherit = "project.project"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    def _pmo_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_pmo")

    def _df_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_df_manager")

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
            raise AccessError(_("Vous n'êtes pas autorisé à créer des projets."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des projets."))
        return super().write(vals)

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des projets."))
        if self._pmo_no_delete():
            raise AccessError(_("Le groupe PMO n'est pas autorisé à supprimer des projets."))
        if self._df_manager_no_delete():
            raise AccessError(_("Le groupe DF MANAGER n'est pas autorisé à supprimer des projets."))
        return super().unlink()


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _dg_read_all_active(self) -> bool:
        return (not self.env.su) and (
            self.env.user.has_group("access_management.group_dg_read_all")
            or self.env.user.has_group("access_management.group_audit")
        )

    def _pmo_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_pmo")

    def _df_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_df_manager")

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
            raise AccessError(_("Vous n'êtes pas autorisé à créer des tâches."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des tâches."))
        return super().write(vals)

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des tâches."))
        if self._pmo_no_delete():
            raise AccessError(_("Le groupe PMO n'est pas autorisé à supprimer des tâches."))
        if self._df_manager_no_delete():
            raise AccessError(_("Le groupe DF MANAGER n'est pas autorisé à supprimer des tâches."))
        return super().unlink()
