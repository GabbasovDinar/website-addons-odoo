odoo.define('website.menu', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var Widget = require('web.Widget');
    var base = require('web_editor.base');

    var _t = core._t;
    var qweb = core.qweb;

    var _get_context = base.get_context;
    base.get_context = function (dict) {
        return _.extend({ 'website_id': $("#website-menu-button").data("website_id")|0 }, _get_context(dict));
    };

    ajax.loadXML('/website_multi_company/static/src/xml/website_templates.xml', qweb);

    var EditorWebsite = Widget.extend({
        start: function() {
            var self = this;
            self.$el.on('click', 'a[data-action]', function(ev) {
                ev.preventDefault();
                self[$(this).data('action')](ev);
            });

            this.$el.find('#website-menu-button').click(function() {
                ajax.jsonRpc( '/website_multi_company/all_websites', 'call').then(function (result) {
                    self.$el.find(".o_website_choice").remove();
                    self.$el.find(".first_divider").before(qweb.render("website_multi_company.all_websites", {websites:result}));

                });
            });
            return this._super();
        },
        change_website: function(event) {
            var website_id = parseInt($(event.target).closest("li").data("website_id"));
            var view_id = parseInt($('html').attr('data-view-xmlid'));
            ajax.jsonRpc( '/website_multi_company/change_website', 'call', {'website_id':website_id, 'view_id':view_id}).then(function (result) {
                var l = window.location;
                var hash = l.hash;
                var url = l.protocol + "//" + result + hash;
                location.replace(url);
            });
        },

    });

    $(document).ready(function() {
        var website_menu = new EditorWebsite();
        website_menu.setElement($("#website-menu"));
        website_menu.start();
    });

    return EditorWebsite;

});
