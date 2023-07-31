
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/grap/grap-odoo-custom/actions/workflows/pre-commit.yml/badge.svg?branch=12.0)](https://github.com/grap/grap-odoo-custom/actions/workflows/pre-commit.yml?query=branch%3A12.0)
[![Build Status](https://github.com/grap/grap-odoo-custom/actions/workflows/test.yml/badge.svg?branch=12.0)](https://github.com/grap/grap-odoo-custom/actions/workflows/test.yml?query=branch%3A12.0)
[![codecov](https://codecov.io/gh/grap/grap-odoo-custom/branch/12.0/graph/badge.svg)](https://codecov.io/gh/grap/grap-odoo-custom)
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
[grap_change_access](grap_change_access/) | 12.0.1.0.16 |  | Add new groups for specific models and change accesses for a number of models.
[grap_change_base_product_mass_addition](grap_change_base_product_mass_addition/) | 12.0.0.1.4 |  | Fix slow call to odoo.tests.Form, used in base_product_mass_addition, for purchase_quick module
[grap_change_data](grap_change_data/) | 12.0.1.0.9 |  | GRAP - Change Data
[grap_change_default](grap_change_default/) | 12.0.1.1.4 |  | GRAP - Change Default
[grap_change_email](grap_change_email/) | 12.0.1.1.4 |  | Change default email template for invoices, sale and purchase orders
[grap_change_precision](grap_change_precision/) | 12.0.1.1.2 |  | Change the precisions names and values of some fields
[grap_change_product_pricelist_direct_print](grap_change_product_pricelist_direct_print/) | 12.0.1.0.1 |  | Display custom fields in Pricelist report
[grap_change_translation](grap_change_translation/) | 12.0.1.2.1 |  | Disable the translation mechanism for a many fields
[grap_change_views](grap_change_views/) | 12.0.1.1.2 |  | GRAP - Change Views
[grap_change_views_account](grap_change_views_account/) | 12.0.1.1.14 |  | GRAP - Change Views Account
[grap_change_views_base](grap_change_views_base/) | 12.0.0.1.5 |  | GRAP - Change Base Views
[grap_change_views_calendar](grap_change_views_calendar/) | 12.0.1.0.3 |  | GRAP - Change Calendar Views
[grap_change_views_mail](grap_change_views_mail/) | 12.0.1.1.2 | [![legalsylvain](https://github.com/legalsylvain.png?size=30px)](https://github.com/legalsylvain) | GRAP - Change Mail Views
[grap_change_views_mrp](grap_change_views_mrp/) | 12.0.1.1.7 |  | GRAP - Change Views MRP
[grap_change_views_partner](grap_change_views_partner/) | 12.0.0.0.20 |  | GRAP - Change Partner Views
[grap_change_views_pos](grap_change_views_pos/) | 12.0.1.1.9 |  | GRAP - Change POS Views
[grap_change_views_product](grap_change_views_product/) | 12.0.0.1.29 |  | GRAP - Change Views Product
[grap_change_views_project](grap_change_views_project/) | 12.0.1.0.4 |  | GRAP - Change Project Views
[grap_change_views_purchase](grap_change_views_purchase/) | 12.0.3.0.3 |  | GRAP - Change Purchase Views
[grap_change_views_sale](grap_change_views_sale/) | 12.0.1.0.11 |  | GRAP - Change Sale Views
[grap_change_views_stock](grap_change_views_stock/) | 12.0.0.1.3 |  | GRAP - Change Stock Views
[grap_cooperative](grap_cooperative/) | 12.0.3.0.6 |  | Add Directories, Companies, Colleges, Peoples, etc.
[grap_index](grap_index/) | 12.0.1.0.3 |  | Add Extra postgresql Indexes
[grap_mrp_dev](grap_mrp_dev/) | 12.0.1.0.1 |  | Install all MRP modules for Grap
[grap_must_have](grap_must_have/) | 12.0.1.1.2 |  | Install must have modules
[grap_qweb_report](grap_qweb_report/) | 12.0.2.0.4 |  | GRAP - Custom Qweb Reports
[grap_theme](grap_theme/) | 12.0.1.3.5 |  | Customize Odoo web User Interface
[mrp_bom_line_has_bom](mrp_bom_line_has_bom/) | 12.0.1.1.1 |  | MRP BoM Line Has BoM
[mrp_bom_print](mrp_bom_print/) | 12.0.1.1.3 |  | Manage the various useful prints for Bill of Materials
[mrp_bom_product_variant](mrp_bom_product_variant/) | 12.0.0.1.2 |  | MRP BoM Product Variant
[mrp_bom_purchase](mrp_bom_purchase/) | 12.0.1.1.4 |  | Handle purchase from your Bill of Materials
[mrp_bom_sale_product_margin](mrp_bom_sale_product_margin/) | 12.0.1.1.5 |  | Handle Sale price for product's bom with margin
[mrp_bom_simple_report](mrp_bom_simple_report/) | 12.0.1.0.1 |  | Print simple report for your Bill of Materials
[mrp_bom_tag](mrp_bom_tag/) | 12.0.1.1.3 |  | Add tags on your BoM to find it easily
[mrp_business](mrp_business/) | 12.0.1.1.6 |  | MRP functions that meet the business needs of GRAP,adapted for food-related professions
[mrp_food](mrp_food/) | 12.0.2.0.1 |  | MRP modules adapted for food-related professions
[product_main_seller](product_main_seller/) | 12.0.1.1.6 |  | Product Attribute - Main seller for a product
[product_supplierinfo_standard_price](product_supplierinfo_standard_price/) | 12.0.0.1.4 |  | Product supplier easily connected to product's standard price
[server_environment_files](server_environment_files/) | 12.0.1.0.5 |  | Add custom CSS and extra text on PoS ticket depending on the environment
[stock_fix_stock_move_line](stock_fix_stock_move_line/) | 12.0.1.1.1 |  | Stock - Fix Stock Move Lines
[stock_merge_quant](stock_merge_quant/) | 12.0.1.1.2 |  | Stock - Merge Quants Tools

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
