/** @odoo-module **/

import { kanbanView } from "@web/views/kanban/kanban_view";
import { KanbanController } from "@web/views/kanban/kanban_controller";
import { registry } from "@web/core/registry";

/**
 * Contrôleur Kanban personnalisé pour les lots de virement bancaire
 * Intercepte la création pour ouvrir le wizard en popup
 * Intercepte l'ouverture pour ouvrir la liste des virements
 */
class BankTransferBatchKanbanController extends KanbanController {
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

    /**
     * @override
     * Ouvre la liste des virements au lieu du formulaire du lot
     */
    async openRecord(record) {
        // Récupérer les informations du lot
        const batchId = record.resId;
        const batchName = record.data.name;
        
        // Ouvrir la liste éditable des virements avec toutes les vues disponibles
        return this.actionService.doAction({
            type: 'ir.actions.act_window',
            name: `Virements du lot: ${batchName}`,
            res_model: 'bank.transfer',
            views: [
                [false, 'list'], 
                [false, 'kanban'], 
                [false, 'form'], 
                [false, 'pivot'], 
                [false, 'graph'], 
                [false, 'calendar']
            ],
            domain: [['batch_id', '=', batchId]],
            context: {
                active_batch_id: batchId,
                default_batch_id: batchId,
            },
            target: 'current',
        });
    }
}

// Vue Kanban personnalisée pour les lots de virement bancaire
const BankTransferBatchKanbanView = {
    ...kanbanView,
    Controller: BankTransferBatchKanbanController,
};

// Enregistrer la vue personnalisée
registry.category("views").add("bank_transfer_batch_kanban", BankTransferBatchKanbanView);

