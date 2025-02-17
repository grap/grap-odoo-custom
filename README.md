
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/grap/grap-odoo-custom/actions/workflows/pre-commit.yml/badge.svg?branch=16.0)](https://github.com/grap/grap-odoo-custom/actions/workflows/pre-commit.yml?query=branch%3A16.0)
[![Build Status](https://github.com/grap/grap-odoo-custom/actions/workflows/test.yml/badge.svg?branch=16.0)](https://github.com/grap/grap-odoo-custom/actions/workflows/test.yml?query=branch%3A16.0)
[![codecov](https://codecov.io/gh/grap/grap-odoo-custom/branch/16.0/graph/badge.svg)](https://codecov.io/gh/grap/grap-odoo-custom)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

# Custom Odoo modules for GRAP

This repository contains Odoo modules developped by the company GRAP for custom needs. They are shared in the hope that it will be useful.

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[fermente_account](fermente_account/) | 16.0.1.1.0 |  | Fermente - Account
[fermente_account_invoice_margin](fermente_account_invoice_margin/) | 16.0.1.0.1 |  | Fermente - Account Invoice Margin
[fermente_account_invoice_triple_discount](fermente_account_invoice_triple_discount/) | 16.0.1.0.1 |  | Fermente - Account Invoice Triple Discount
[fermente_account_menu_invoice_refund](fermente_account_menu_invoice_refund/) | 16.0.1.0.1 |  | Fermente - Account Menu Invoice Refund
[fermente_account_move_name_sequence](fermente_account_move_name_sequence/) | 16.0.1.0.1 |  | Fermente - Account Move Name Sequence
[fermente_base](fermente_base/) | 16.0.1.0.0 |  | Fermente - Base
[fermente_hr](fermente_hr/) | 16.0.1.0.0 |  | Fermente - Human Ressources
[fermente_main_menu](fermente_main_menu/) | 16.0.1.0.0 |  | Fermente - Main Menu
[fermente_mrp](fermente_mrp/) | 16.0.1.0.1 |  | Fermente - MRP
[fermente_mrp_bom_form_view](fermente_mrp_bom_form_view/) | 16.0.1.0.1 |  | Fermente - MRP BoM Form View
[fermente_pos](fermente_pos/) | 16.0.2.0.0 |  | Fermente - Point Of Sale
[fermente_product](fermente_product/) | 16.0.1.1.1 |  | Fermente - Product
[fermente_product_category_active](fermente_product_category_active/) | 16.0.1.1.1 |  | Fermente - Product Category Active
[fermente_product_margin_classification](fermente_product_margin_classification/) | 16.0.1.0.1 |  | Fermente - Product Margin Classification
[fermente_stock](fermente_stock/) | 16.0.1.1.0 |  | Fermente - Stock
[fermente_web_environment_ribbon](fermente_web_environment_ribbon/) | 16.0.1.0.0 |  | Fermente - Web Environment Ribbon
[mrp_bom_report_allergen](mrp_bom_report_allergen/) | 16.0.1.0.0 |  | Manage the various useful prints for Bill of Materials
[mrp_bom_weight](mrp_bom_weight/) | 16.0.1.0.1 |  | MRP BoM Weight
[mrp_bom_wizard_production](mrp_bom_wizard_production/) | 16.0.1.2.0 |  | Wizard linked to Bill of Materials to help your production.
[mrp_business](mrp_business/) | 16.0.1.1.1 |  | MRP functions that meet the business needs of GRAP,adapted for food-related professions
[mrp_sale_grouped](mrp_sale_grouped/) | 16.0.1.0.1 |  | Quickly manage what you need to produce thanks to grouped sales
[server_environment_files](server_environment_files/) | 16.0.1.0.0 |  | Add custom CSS and extra text on PoS ticket depending on the environment

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to GRAP
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----

## About GRAP

<p align="center">
   <img src="http://www.grap.coop/wp-content/uploads/2016/11/GRAP.png" width="200"/>
</p>

GRAP, [Groupement Régional Alimentaire de Proximité](http://www.grap.coop) is a
french company which brings together activities that sale food products in the
region Rhône Alpes. We promote organic and local food, social and solidarity
economy and cooperation.

The GRAP IT Team promote Free Software and developp all the Odoo modules under
AGPL-3 Licence.

You can find all these modules here:

* on the [OCA Apps Store](https://odoo-community.org/shop?&search=GRAP)
* on the [Odoo Apps Store](https://www.odoo.com/apps/modules/browse?author=GRAP).
* on [Odoo Code Search](https://odoo-code-search.com/ocs/search?q=author%3AOCA+author%3AGRAP)

You can also take a look on the following repositories:

* [grap-odoo-incubator](https://github.com/grap/grap-odoo-incubator)
* [grap-odoo-business](https://github.com/grap/grap-odoo-business)
* [grap-odoo-business-supplier-invoice](https://github.com/grap/grap-odoo-business-supplier-invoice)
* [odoo-addons-logistics](https://github.com/grap/odoo-addons-logistics)
* [odoo-addons-cae](https://github.com/grap/odoo-addons-cae)
* [odoo-addons-intercompany-trade](https://github.com/grap/odoo-addons-intercompany-trade)
* [odoo-addons-multi-company](https://github.com/grap/odoo-addons-multi-company)
* [odoo-addons-company-wizard](https://github.com/grap/odoo-addons-company-wizard)
