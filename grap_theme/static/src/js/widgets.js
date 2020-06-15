/** ***************************************************************************
    Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
    @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
******************************************************************************/

odoo.define("grap_theme.widgets", function (require) {
    "use strict";

    var SwitchCompanyMenu = require("web.SwitchCompanyMenu");

    var SwitchCompanyMenuWidget = SwitchCompanyMenu.include({
        start: function () {
            var session = this.getSession();
            return this._super.apply(this, arguments).then(function () {
                var company_avatar_src = session.url('/web/image', {
                    model:'res.company',
                    field: 'logo',
                    id: session.company_id,
                });
                self.$('.oe_topbar_company_avatar').attr('src', company_avatar_src);
                return $.when();
            });
        },
    });
});
