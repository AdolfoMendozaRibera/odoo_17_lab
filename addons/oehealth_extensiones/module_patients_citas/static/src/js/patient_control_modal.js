odoo.define('module_patients_citas.patient_control_modal', ['web.AbstractAction', 'web.core', 'web.rpc'], function (require) {
    'use strict';
    console.log('✅ patient_control_modal.js iniciando (v2)...');

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var PatientControlModal = AbstractAction.extend({
        init: function (parent, action) {
            this._super(parent, action);
            this.action = action;
            this.selectedPlan = null;
            this.serviceTypes = [];
            console.log('✓ PatientControlModal inicializado');
        },

        willStart: function () {
            var self = this;
            console.log('📡 Obteniendo tipos de servicios...');
            return rpc.query({
                route: '/patient_control/get_service_types'
            }).then(function (result) {
                self.serviceTypes = result.service_types || [];
                console.log('✓ Servicios cargados:', self.serviceTypes);
            }).catch(function (error) {
                console.error('❌ Error obteniendo servicios:', error);
            });
        },

        start: function () {
            this._super.apply(this, arguments);
            console.log('🚀 Renderizando modal...');
            this.renderModal();
            this.attachEvents();
        },

        renderModal: function () {
            var self = this;
            var modalHTML = '<div style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; background: #f5f5f5; padding: 20px;">' +
                '<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); display: flex; justify-content: center; align-items: center; z-index: 1050;">' +
                '<div style="background: white; border-radius: 8px; box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2); max-width: 700px; width: 90%; max-height: 90vh; overflow-y: auto;">' +
                '<div style="display: flex; justify-content: space-between; align-items: center; padding: 24px 20px; border-bottom: 1px solid #e9ecef; background: #f8f9fa;">' +
                '<h2 style="font-size: 18px; font-weight: 600; margin: 0; color: #333;">Seleccionar Tipo de Servicio</h2>' +
                '<button id="closePlanModalBtn" style="background: none; border: none; font-size: 28px; cursor: pointer; color: #999; padding: 0; width: 32px; height: 32px;">&times;</button>' +
                '</div>' +
                '<div style="padding: 24px 20px;">' +
                '<p style="margin: 0 0 20px 0; color: #666; font-size: 14px; line-height: 1.5;">Seleccione el tipo de servicio que desea agendar:</p>' +
                '<div id="planCards" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;"></div>' +
                '</div>' +
                '<div style="display: flex; justify-content: flex-end; gap: 12px; padding: 16px 20px; border-top: 1px solid #e9ecef; background: #f8f9fa;">' +
                '<button id="cancelPlanBtn" style="padding: 10px 20px; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; font-size: 13px; background: white; color: #333;">Cancelar</button>' +
                '<button id="confirmPlanBtn" disabled style="padding: 10px 20px; border: 1px solid #007bff; border-radius: 4px; cursor: pointer; font-size: 13px; background: #007bff; color: white; opacity: 0.5;">Continuar</button>' +
                '</div>' +
                '</div>' +
                '</div>' +
                '</div>';

            self.$el.html(modalHTML);
            self.renderServiceTypes();
        },

        renderServiceTypes: function () {
            var self = this;
            var $planCards = this.$('#planCards');
            $planCards.empty();

            self.serviceTypes.forEach(function (service) {
                var cardHTML = '<div class="plan-card" data-plan="' + service.id + '" style="border: 2px solid #ddd; border-radius: 8px; padding: 24px 16px; text-align: center; cursor: pointer; transition: all 0.3s ease; background: #fff;">' +
                    '<div style="font-size: 36px; margin-bottom: 12px;">' + service.icon + '</div>' +
                    '<div style="font-weight: 600; font-size: 15px; margin-bottom: 8px; color: #333;">' + service.name + '</div>' +
                    '<div style="font-size: 13px; color: #666; line-height: 1.5;">' + service.description + '</div>' +
                    '</div>';
                $planCards.append(cardHTML);
            });
        },

        attachEvents: function () {
            var self = this;
            var $closeBtn = this.$('#closePlanModalBtn');
            var $cancelBtn = this.$('#cancelPlanBtn');
            var $confirmBtn = this.$('#confirmPlanBtn');
            var $planCards = this.$('#planCards');

            $closeBtn.on('click', function () { self.closeModal(); });
            $cancelBtn.on('click', function () { self.closeModal(); });
            $confirmBtn.on('click', function () { self.confirmSelection(); });

            $planCards.on('click', '.plan-card', function () {
                self.selectPlan($(this), $confirmBtn);
            });
        },

        selectPlan: function ($card, $confirmBtn) {
            this.$('.plan-card').css({
                'border-color': '#ddd',
                'background': '#fff',
                'box-shadow': 'none'
            });

            $card.css({
                'border-color': '#007bff',
                'background': '#f0f7ff',
                'box-shadow': '0 4px 12px rgba(0, 123, 255, 0.25)'
            });

            this.selectedPlan = $card.attr('data-plan');
            console.log('✓ Plan seleccionado:', this.selectedPlan);

            $confirmBtn.prop('disabled', false).css('opacity', '1');
        },

        confirmSelection: function () {
            var self = this;

            if (!this.selectedPlan) {
                alert('Por favor selecciona un tipo de servicio');
                return;
            }

            // Abrir formulario de paciente con el plan preseleccionado
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'oeh.medical.patient',
                view_mode: 'form',
                views: [[false, 'form']],
                target: 'current',
                context: {
                    'default_service_plan': this.selectedPlan
                }
            });
        },

        closeModal: function () {
            this.do_action({ type: 'ir.actions.client', tag: 'reload' });
        }
    });

    core.action_registry.add('patient_control_service_modal', PatientControlModal);
    console.log('✅ Action registrado: patient_control_service_modal');

    return PatientControlModal;
});