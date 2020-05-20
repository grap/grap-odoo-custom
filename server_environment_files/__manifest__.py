# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    "name": "GRAP - Configuration Environment Files",
    "summary": "Add custom CSS and extra text on PoS ticket"
    " depending on the environment",
    "version": "12.0.1.0.0",
    "category": "GRAP - Custom",
    "author": "GRAP",
    "license": "AGPL-3",
    "depends": ["server_environment_ir_config_parameter", "pos_environment"],
    "data": ["views/templates.xml"],
    "installable": True,
}
