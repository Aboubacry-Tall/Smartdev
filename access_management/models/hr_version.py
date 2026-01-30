# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError


class HrVersion(models.Model):
    _inherit = "hr.version"

    def _rh_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_rh")

    def _paie_read_only(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_paie")

    @api.model_create_multi
    def create(self, vals_list):
        if self._paie_read_only():
            raise AccessError(_("Le groupe PAIE n'est pas autorisé à créer des contrats."))
        return super().create(vals_list)

    def write(self, vals):
        if self._paie_read_only():
            raise AccessError(_("Le groupe PAIE n'est pas autorisé à modifier des contrats."))
        return super().write(vals)

    def unlink(self):
        if self._rh_no_delete():
            raise AccessError(_("Le groupe RH n'est pas autorisé à supprimer des contrats."))
        if self._paie_read_only():
            raise AccessError(_("Le groupe PAIE n'est pas autorisé à supprimer des contrats."))
        return super().unlink()
