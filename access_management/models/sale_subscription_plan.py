# pylint: disable=import-error

from odoo import _, models
from odoo.exceptions import AccessError


class SaleSubscriptionPlan(models.Model):
    _inherit = "sale.subscription.plan"

    def _finance_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_finance")

    def unlink(self):
        if self._finance_no_delete():
            raise AccessError(_("Le groupe FINANCE n'est pas autorisé à supprimer des plans d'abonnement."))
        return super().unlink()
