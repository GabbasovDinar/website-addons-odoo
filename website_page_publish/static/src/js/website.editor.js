odoo.define('website_blog.new_blog_post', function (require) {
    "use strict";

    var contentMenu = require('website.contentMenu');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var base = require('web_editor.base');
    var website = require('website.website');

    var _t = core._t;
    var qweb = core.qweb;

    ajax.loadXML('/website_page_publish/static/src/xml/website.xml', qweb);

    contentMenu.TopBar.include({
        publish_page: function () {
            var self = this;
            var context = base.get_context();
            self.mo_id = self.getMainObject().id;

            ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                model: 'ir.ui.view',
                method: 'search_read',
                args: [],
                kwargs: {
                    fields: ['is_publish'],
                    domain: [['id', '=', self.mo_id]],
                    context: base.get_context()
                }
            }).then(function (res) {
                var is_publish = res[0].is_publish;
                website.prompt({
                    id: "editor_publish_page",
                    window_title: _t("Publish Page"),
                    window_body: is_publish ? _t('This page has been published.') : _t('This page is not published.'),
                    is_publish: is_publish,
                }, 'website.publish_page').then(function (val, field) {
                    val = field.is(':checked');
                    ajax.jsonRpc('/web/dataset/call_kw', 'call', {
                        model: 'website',
                        method: 'publish_page',
                        args: [
                            self.mo_id,
                            val,
                        ],
                        kwargs: {
                            context: context
                        },
                    }).then(function () {
                        window.location.reload();
                    });
                });
            });
        },
    });

    return contentMenu;
});
