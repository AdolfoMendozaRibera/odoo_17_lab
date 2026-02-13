/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

export class ServiceSelectionModal extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.action = useService("action");
        
        this.serviceTypes = [];
        this.selectedPlan = null;
        
        this.loadServiceTypes();
    }
    
    async loadServiceTypes() {
        try {
            const result = await this.rpc('/patient_control/get_service_types');
            this.serviceTypes = result.service_types || [];
        } catch (error) {
            console.error('Error loading service types:', error);
            this.notification.add(_t('Error loading services'), {
                type: 'danger',
            });
        }
    }
    
    selectPlan(serviceId) {
        this.selectedPlan = serviceId;
    }
    
    async confirmSelection() {
        if (!this.selectedPlan) {
            this.notification.add(_t('Please select a service type'), {
                type: 'warning',
            });
            return;
        }
        
        try {
            const result = await this.rpc('/patient_control/create_appointment', {
                service_type: this.selectedPlan,
                patient_id: this.props.context.active_id || null,
            });
            
            if (result.success) {
                this.notification.add(result.message, {
                    type: 'success',
                });
                this.action.doAction({ type: 'ir.actions.client', tag: 'reload' });
            } else {
                this.notification.add(_t('Error: ') + result.message, {
                    type: 'danger',
                });
            }
        } catch (error) {
            console.error('Error creating appointment:', error);
            this.notification.add(_t('Error creating appointment'), {
                type: 'danger',
            });
        }
    }
    
    closeModal() {
        this.action.doAction({ type: 'ir.actions.client', tag: 'reload' });
    }
}

ServiceSelectionModal.template = "module_patients_citas.ServiceSelectionModal";
