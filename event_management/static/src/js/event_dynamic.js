odoo.define('dynamic_snippet_blog.dynamic', function (require) {
   var PublicWidget = require('web.public.widget');
   var rpc = require('web.rpc');
   var Dynamic = PublicWidget.Widget.extend({
       selector: '.dynamic_snippet_blog',
       start: function () {

           var self = this;
           rpc.query({
               route: '/latest_events',
               params: {},
           }).then(data=>{
                let html = ''
                data.forEach(i=>{
                    html += '<div class="card m-2" style="width: 18rem;">'+
                         '<img class="card-img-top" src="/event_management/static/src/img/good.jpg"," alt="Card image cap">'+
                        '<div class="card-body">'+
                            '<h5 class="card-title">'+'<a href="/events_website/'+i.id+'" class="card-link">'+i.name+'</a></h5>'+
                        '</div>'+
                    '</div>'
                })
                self.$('#latest_event').append(html);
           })
       },
   });
   PublicWidget.registry.dynamic_snippet_blog = Dynamic;
   return Dynamic;
});