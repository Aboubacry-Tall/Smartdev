/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";

/**
 * Contrôleur Liste personnalisé pour les virements bancaires d'un lot
 * Affiche les virements avec des boutons d'action dans le header
 */
export class BankTransferBatchListViewController extends ListController {

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    /**
     * Retourne à la vue du lot (formulaire)
     */
    async onReturnToBatch() {
        const batchId = this.props.context.active_batch_id || this.props.context.default_batch_id;
        
        if (!batchId) {
            this.notification.add(
                "Erreur : Impossible de retrouver le lot.",
                { type: "danger" }
            );
            return;
        }
        
        return this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'bank.transfer.batch',
            res_id: batchId,
            views: [[false, 'form']],
            target: 'current',
        });
    }

    /**
     * Exporte les virements vers Excel
     */
    async onExportExcel() {
        const batchId = this.props.context.active_batch_id || this.props.context.default_batch_id;
        
        if (!batchId) {
            this.notification.add(
                "Erreur : Impossible de retrouver le lot.",
                { type: "danger" }
            );
            return;
        }
        
        try {
            // Appeler une méthode Python pour générer l'export Excel
            const result = await this.orm.call(
                "bank.transfer.batch",
                "action_export_transfers_excel",
                [batchId]
            );
            
            if (result && result.type === 'ir.actions.act_url') {
                return this.actionService.doAction(result);
            }
            
            this.notification.add(
                "Export Excel en cours de préparation...",
                { type: "info" }
            );
        } catch (error) {
            this.notification.add(
                `Erreur lors de l'export : ${error.message}`,
                { type: "danger" }
            );
        }
    }

    /**
     * Importe les salaires depuis un fichier Excel
     */
    async onImportSalaries() {
        const batchId = this.props.context.active_batch_id || this.props.context.default_batch_id;
        
        if (!batchId) {
            this.notification.add(
                "Erreur : Impossible de retrouver le lot.",
                { type: "danger" }
            );
            return;
        }
        
        // Ouvrir un wizard d'import
        return this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: 'Importer les salaires',
            res_model: 'bank.transfer.import.wizard',
            views: [[false, 'form']],
            target: 'new',
            context: {
                default_batch_id: batchId,
            },
        });
    }
}

// Vue Liste personnalisée pour les virements d'un lot
export const bankTransferEditableListView = {
    ...listView,
    Controller: BankTransferBatchListViewController,
};

// Enregistrer la vue personnalisée
registry.category("views").add("bank_transfer_editable_list", bankTransferEditableListView);

