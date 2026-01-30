# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError

from lxml import etree


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _pmo_timesheet_no_create(self) -> bool:
        """PMO : lecture et validation (write) uniquement, pas de création de feuilles de temps."""
        return (not self.env.su) and self.env.user.has_group("access_management.group_pmo")

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)

        if self._pmo_timesheet_no_create() and view_type in {"list", "kanban", "form"}:
            node = etree.fromstring(result["arch"])
            node.set("create", "0")
            result["arch"] = etree.tostring(node, encoding="unicode")

        return result

    @api.model_create_multi
    def create(self, vals_list):
        if self._pmo_timesheet_no_create():
            raise AccessError(_("Le groupe PMO n'est pas autorisé à créer des feuilles de temps (validation uniquement)."))
        return super().create(vals_list)
