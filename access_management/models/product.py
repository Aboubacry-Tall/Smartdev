# pylint: disable=import-error

from odoo import _, api, models
from odoo.exceptions import AccessError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _df_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_df_manager")

    def _dh_read_only(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_dh")

    @api.model_create_multi
    def create(self, vals_list):
        if self._dh_read_only():
            raise AccessError(_("Le groupe DH n'est pas autorisé à créer des produits."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dh_read_only():
            raise AccessError(_("Le groupe DH n'est pas autorisé à modifier des produits."))
        return super().write(vals)

    def unlink(self):
        if self._dh_read_only():
            raise AccessError(_("Le groupe DH n'est pas autorisé à supprimer des produits."))
        if self._df_manager_no_delete():
            raise AccessError(_("Le groupe DF MANAGER n'est pas autorisé à supprimer des produits."))
        return super().unlink()


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _df_manager_no_delete(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_df_manager")

    def _dh_read_only(self) -> bool:
        return (not self.env.su) and self.env.user.has_group("access_management.group_dh")

    @api.model_create_multi
    def create(self, vals_list):
        if self._dh_read_only():
            raise AccessError(_("Le groupe DH n'est pas autorisé à créer des variantes de produit."))
        return super().create(vals_list)

    def write(self, vals):
        if self._dh_read_only():
            raise AccessError(_("Le groupe DH n'est pas autorisé à modifier des variantes de produit."))
        return super().write(vals)

    def unlink(self):
        if self._dh_read_only():
            raise AccessError(_("Le groupe DH n'est pas autorisé à supprimer des variantes de produit."))
        if self._df_manager_no_delete():
            raise AccessError(_("Le groupe DF MANAGER n'est pas autorisé à supprimer des variantes de produit."))
        return super().unlink()
