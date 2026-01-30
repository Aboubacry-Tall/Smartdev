# pylint: disable=import-error

from odoo import _, models
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _bd_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_bd_manager")

    def unlink(self):
        if self._bd_manager_no_delete():
            raise AccessError(_("Le groupe BD MANAGER n'est pas autorisé à supprimer des clients/contacts."))
        return super().unlink()
