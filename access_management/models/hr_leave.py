# pylint: disable=import-error

from odoo import _, models
from odoo.exceptions import AccessError


class HrLeave(models.Model):
    _inherit = "hr.leave"

    def _rh_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_rh")

    def unlink(self):
        if self._rh_no_delete():
            raise AccessError(_("Le groupe RH n'est pas autorisé à supprimer des congés."))
        return super().unlink()


class HrLeaveAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    def _rh_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_rh")

    def unlink(self):
        if self._rh_no_delete():
            raise AccessError(_("Le groupe RH n'est pas autorisé à supprimer des allocations de congés."))
        return super().unlink()
