/** @odoo-module **/

import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { registry } from "@web/core/registry";

/**
 * Contrôleur Liste personnalisé pour les lots de virement bancaire
 * Intercepte la création pour ouvrir le wizard en popup
 */
class BankTransferBatchListController extends ListController {
    /**
     * @override
     * Ouvre le wizard en popup au lieu de la vue form standard
     */
    async createRecord() {
        // Ouvrir le wizard étape 1 en popup
        return this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'bank.transfer.batch.wizard.step1',
            views: [[false, 'form']],
            target: 'new',
            context: {
                dialog_size: 'medium',
            },
        });
    }
}

// Vue Liste personnalisée pour les lots de virement bancaire
const BankTransferBatchListView = {
    ...listView,
    Controller: BankTransferBatchListController,
};

// Enregistrer la vue personnalisée
registry.category("views").add("bank_transfer_batch_list", BankTransferBatchListView);

