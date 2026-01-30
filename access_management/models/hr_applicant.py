# pylint: disable=import-error

from odoo import _, models
from odoo.exceptions import AccessError


class HrApplicant(models.Model):
    _inherit = "hr.applicant"

    def _rh_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_rh")

    def unlink(self):
        if self._rh_no_delete():
            raise AccessError(_("Le groupe RH n'est pas autorisé à supprimer des candidatures."))
        return super().unlink()
