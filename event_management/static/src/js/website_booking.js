odoo.define('event_management.example', function (require) {
"use strict";
var Dialog = require('web.Dialog');
var rpc = require('web.rpc');
var core = require('web.core');
var _t = core._t;
const publicWidget = require('web.public.widget')
publicWidget.registry.websiteEvents = publicWidget.Widget.extend({
selector:'#wrap',
events: {
'change #event_end_date': '_alert_onclick',
'change #name': '_relate_field',
},
_alert_onclick: function (ev) {
    var b_date = $("#event_begin_date").val();
    var e_date = $("#event_end_date").val();
    var start_date = Date.parse(b_date);
    var end_date = Date.parse(e_date)
        if(b_date && e_date){
            if(b_date>e_date){
                $("#event_end_date").val('');
                Dialog.alert(self, _t("invalid date"), {
                title: _t('onclick'),
                });
            }
            else{
                var diffDays = new Date(end_date - start_date)/1000/60/60/24;
                $("#event_duration").val(diffDays+1);
            }
        }
},
_relate_field: function (ev) {
        var p_name = this.$("#name").val()
        var partner_id = $("#browse_partner option[value='"+p_name+"']").attr('data-id')
        if (partner_id){
            this.$("#partner_hide").val(partner_id)
        }
        else{
            this.$("#partner_hide").val(p_name)
        }
        console.log(this.$("#partner_hide").val())
        rpc.query({
               route: '/event_relate',
               params: {'key':partner_id},
           }).then(data=>{
                var phone = data['phone']
                var email = data['email']
                if (phone){
                    $("#phone").val(data['phone']);
                }
                if (email){
                    $("#email").val(data['email']);
                }
           })
},
})
});
