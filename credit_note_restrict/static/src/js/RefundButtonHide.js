odoo.define('credit_note_restrict.RefundButtonHide', function (require) {
    'use strict';

    const ButtonRefund = require('point_of_sale.RefundButton');
    const Registries = require('point_of_sale.Registries');


    const POSRefundButtonCustomHide = (ButtonRefund) =>
        class extends ButtonRefund {
            constructor() {
                console.log("js:: en mi funcion")

                super(...arguments);

                const botones_control = document.getElementsByClassName("control-button")[1];
                console.log("Botones control")
                console.log(botones_control)
                for (const boton in botones_control) {
                    console.log("js:: boton name")
                    console.log(boton.innerText)
                    if(boton.textContent == " Reembolso"){
                        boton.style.visibility = "hidden";
                    }
                }


            }
        };

    Registries.Component.extend(ButtonRefund, POSRefundButtonCustomHide);

    return ButtonRefund;
});