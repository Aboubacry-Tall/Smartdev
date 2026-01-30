# pylint: disable=import-error

from odoo import _, models
from odoo.exceptions import AccessError


class ProjectMilestone(models.Model):
    _inherit = "project.milestone"

    def _df_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_df_manager")

    def unlink(self):
        if self._df_manager_no_delete():
            raise AccessError(_("Le groupe DF MANAGER n'est pas autorisé à supprimer des jalons (roadmap)."))
        return super().unlink()
