odoo.define('event_management.example', function (require) {
"use strict";
var Dialog = require('web.Dialog');
var core = require('web.core');
var _t = core._t;
const publicWidget = require('web.public.widget')
publicWidget.registry.websiteEvents = publicWidget.Widget.extend({
selector:'#wrap',
events: {
'change #event_end_date': '_alert_onclick',
},
_alert_onclick: function (ev) {
    var b_date = $("#event_begin_date").val();
    var e_date = $("#event_end_date").val();
    var start_date = Date.parse(b_date);
    var end_date = Date.parse(e_date)
//    console.log(b_date)
//    console.log(e_date)
        if(b_date && e_date){
            if(b_date>e_date){
                $("#event_end_date").val('');
                Dialog.alert(self, _t("invalid date"), {
                title: _t('onclick'),
                });
            }
            else{
                var diffDays = new Date(end_date - start_date)/1000/60/60/24;
//                console.log(diffDays)
                $("#event_duration").val(diffDays+1);
            }
        }
},
})
});
console.log("ok")