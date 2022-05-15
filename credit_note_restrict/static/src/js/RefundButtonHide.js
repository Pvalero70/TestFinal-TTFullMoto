odoo.define('credit_note_restrict.RefundButtonHide', function (require) {
    'use strict';

    const ButtonRefund = require('point_of_sale.RefundButton');
    const Registries = require('point_of_sale.Registries');


    const POSRefundButtonCustomHide = (ButtonRefund) =>
        class extends ButtonRefund {
            constructor() {
                console.log("js:: en mi funcion")

                super(...arguments);
                this.hide();
                console.log("js:: en mi funcion")

            }
        };

    Registries.Component.extend(ButtonRefund, POSRefundButtonCustomHide);

    return ButtonRefund;
});