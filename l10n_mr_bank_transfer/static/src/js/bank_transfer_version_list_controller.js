/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

/**
 * Contrôleur Liste personnalisé pour la sélection des versions (hr.version)
 * lors de la création d'un lot de virement bancaire
 */
export class BankTransferVersionListController extends ListController {

    setup() {
        super.setup();
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.notification = useService("notification");
        this.state = useState({
            disabled: false,
        });
    }

    /**
     * Ferme la vue et retourne à la vue précédente
     */
    async onClose() {
        return this.actionService.doAction({type: "ir.actions.act_window_close"});
    }

    /**
     * Crée le lot de virement avec les versions sélectionnées
     */
    async createBatch() {
        this.state.disabled = true;
        
        try {
            // Récupérer les IDs des versions sélectionnées
            const selectedVersionIds = await this.model.root.getResIds(true);
            
            if (selectedVersionIds.length < 1) {
                this.notification.add(
                    "Veuillez sélectionner au moins un employé.",
                    { type: "warning" }
                );
                return;
            }
            
            // Récupérer les informations du lot depuis le contexte
            const batchName = this.props.context.default_batch_name;
            const batchDate = this.props.context.default_batch_date;
            
            if (!batchName || !batchDate) {
                this.notification.add(
                    "Erreur : Informations du lot manquantes.",
                    { type: "danger" }
                );
                return;
            }
            
            // Appeler la méthode Python pour créer le lot
            const result = await this.orm.call(
                "bank.transfer.batch",
                "create_batch_from_versions",
                [],
                {
                    name: batchName,
                    date: batchDate,
                    version_ids: selectedVersionIds,
                }
            );
            
            // Fermer la vue
            await this.onClose();
            
            // Ouvrir la liste des virements du lot créé
            return this.actionService.doAction({
                type: 'ir.actions.act_window',
                name: `Virements du lot: ${batchName}`,
                res_model: 'bank.transfer',
                views: [[false, 'list'], [false, 'form']],
                domain: [['batch_id', '=', result.batch_id]],
                context: {
                    active_batch_id: result.batch_id,
                    default_batch_id: result.batch_id,
                },
                target: 'current',
            });
            
        } catch (error) {
            this.notification.add(
                `Erreur lors de la création du lot : ${error.message}`,
                { type: "danger" }
            );
        } finally {
            this.state.disabled = false;
        }
    }

    /**
     * Retourne à l'étape 1 du wizard
     */
    async onBack() {
        const batchName = this.props.context.default_batch_name;
        const batchDate = this.props.context.default_batch_date;
        
        return this.actionService.doAction({
            type: 'ir.actions.act_window',
            res_model: 'bank.transfer.batch.wizard.step1',
            views: [[false, 'form']],
            target: 'new',
            context: {
                default_name: batchName,
                default_date: batchDate,
                dialog_size: 'medium',
            },
        });
    }

    /**
     * Crée un lot vide et ferme le wizard
     */
    async createEmptyBatchAndClose() {
        this.state.disabled = true;
        
        try {
            // Récupérer les informations du lot depuis le contexte
            const batchName = this.props.context.default_batch_name;
            const batchDate = this.props.context.default_batch_date;
            
            if (!batchName || !batchDate) {
                this.notification.add(
                    "Erreur : Informations du lot manquantes.",
                    { type: "danger" }
                );
                this.state.disabled = false;
                return;
            }
            
            // Créer un lot vide
            await this.orm.create(
                "bank.transfer.batch",
                [{
                    name: batchName,
                    date: batchDate,
                }]
            );
            
            // Notification de succès
            this.notification.add(
                `Lot "${batchName}" créé avec succès.`,
                { type: "success" }
            );
            
            // Fermer le wizard
            await this.onClose();
            
            // Actualiser la vue Kanban des lots avec toutes les vues disponibles
            return this.actionService.doAction({
                type: 'ir.actions.act_window',
                res_model: 'bank.transfer.batch',
                name: 'Lots de virement',
                view_mode: 'kanban,list,form,pivot,graph,calendar',
                views: [
                    [false, 'kanban'], 
                    [false, 'list'], 
                    [false, 'form'], 
                    [false, 'pivot'], 
                    [false, 'graph'], 
                    [false, 'calendar']
                ],
                target: 'current',
            });
            
        } catch (error) {
            this.notification.add(
                `Erreur lors de la création du lot : ${error.message}`,
                { type: "danger" }
            );
            this.state.disabled = false;
        }
    }
}

// Vue Liste personnalisée pour la sélection des versions
export const bankTransferVersionListView = {
    ...listView,
    Controller: BankTransferVersionListController,
    buttonTemplate: "l10n_mr_bank_transfer.BankTransferVersionListController.Buttons",
};

// Enregistrer la vue personnalisée
registry.category("views").add("bank_transfer_version_list", bankTransferVersionListView);

