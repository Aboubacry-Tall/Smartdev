# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError

from lxml import etree


class MarketingCampaign(models.Model):
    _inherit = "marketing.campaign"

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
            raise AccessError(_("Vous n'êtes pas autorisé à créer des campagnes marketing."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des campagnes marketing."))
        return super().write(vals)

    def _dh_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_dh")

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des campagnes marketing."))
        if self._dh_no_delete():
            raise AccessError(_("Le groupe DH n'est pas autorisé à supprimer des campagnes marketing."))
        return super().unlink()


class MarketingActivity(models.Model):
    _inherit = "marketing.activity"

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
            raise AccessError(_("Vous n'êtes pas autorisé à créer des activités marketing."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à modifier des activités marketing."))
        return super().write(vals)

    def _dh_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_dh")

    def unlink(self):
        if self._dg_read_all_active():
            raise AccessError(_("Vous n'êtes pas autorisé à supprimer des activités marketing."))
        if self._dh_no_delete():
            raise AccessError(_("Le groupe DH n'est pas autorisé à supprimer des activités marketing."))
        return super().unlink()


class MarketingParticipant(models.Model):
    _inherit = "marketing.participant"

    def _dh_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_dh")

    def unlink(self):
        if self._dh_no_delete():
            raise AccessError(_("Le groupe DH n'est pas autorisé à supprimer des participants marketing."))
        return super().unlink()
