/** ***************************************************************************
    Copyright (C) 2020 - Today: GRAP (http://www.grap.coop)
    @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
******************************************************************************/

odoo.define("grap_change_views_mail.systray", function (require) {
    "use strict";

    var SystrayMenu = require('web.SystrayMenu');

    var newItems = [];
    _.each(SystrayMenu.Items, function (WidgetClass) {
        if (["mail.systray.MessagingMenu", "mail.systray.ActivityMenu"].indexOf(
                WidgetClass.prototype.template) === -1) {
            newItems.push(WidgetClass);
        }
    });
    SystrayMenu.Items = newItems;

});
