odoo.define('pos_custom_settle_due.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('pos_customs.PaymentScreenC');
    const Registries = require('point_of_sale.Registries');
    const { float_is_zero } = require('web.utils');
    // const { patch } = require('web.utils');

    // patch(PaymentScreen.prototype, "prototype patch", {
    //     async validateOrder() {
    //         console.log('###Sobre escribe nuevo###')
    //     }
    // });

    const PosSettleDuePaymentScreenCustom = (PaymentScreen) =>
        class extends PaymentScreen {
            

            // async validateOrder() {
            //     console.log('###Sobre escribe###')

            //     const order = this.currentOrder;
                
            //     if (!order.is_payment_invoice){
            //         return super.validateOrder(...arguments);
            //     }
            //     else{
            //         const change = order.get_change();
            //         const paylaterPaymentMethod = this.env.pos.payment_methods.filter(
            //             (method) =>
            //                 this.env.pos.config.payment_method_ids.includes(method.id) && method.type == 'pay_later'
            //         )[0];
            //         const existingPayLaterPayment = order
            //             .get_paymentlines()
            //             .find((payment) => payment.payment_method.type == 'pay_later');
                    
            //         console.log(order)
            //         console.log(change)
            //         console.log(paylaterPaymentMethod)
            //         console.log(existingPayLaterPayment)
    
            //         // this.currentOrder.finalized = true;
    
            //         // order.destroy({ reason: 'abandon' });
    
            //         // this.showScreen(this.nextScreen);
    
            //         // return
            //         console.log(arguments)
    
            //         const res = super.validateOrder(...arguments);
    
            //         console.log("Despues de la validacion")
    
            //         // const paylaterPayment = order.add_paymentline(paylaterPaymentMethod);
            //         // paylaterPayment.set_amount(change);
    
            //         return res
            //     }

                
            // };
            async _finalizeValidation() {
                
                console.log("FINALIZE VALIDATION")
                this.currentOrder.prueba = 123
                console.log(this.currentOrder)

                return super._finalizeValidation(...arguments);
            };
        };

    Registries.Component.extend(PaymentScreen, PosSettleDuePaymentScreenCustom);

    return PaymentScreen;
});

