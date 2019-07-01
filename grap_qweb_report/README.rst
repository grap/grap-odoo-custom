.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===================
GRAP - QWeb Reports
===================

* Redefine default odoo qweb reports for GRAP.
* Add some computed field on models for that purpose.

Models changes
--------------

* account.invoice
    * add ```has_discount``` field

* account.tax
    * add ```report_short_code``` field

* product.product
    * add ```report_extra_food_info``` field that maps ```country_id``` and
      ```fresh_category``` field
    * add ```report_label_ids_info``` field that maps ```label_ids.code```
      field

report changes
--------------

* account.invoice
    * optionaly display ```discount``` column on invoice lines.
    * display short text for taxes.
    * display short text for labels.
    * allway display unit price vat Exlc.

* purchase.order
    * display short text for taxes.

* sale.order
    * display short text for taxes.

* pos.order bill
    * display VAT details
    * display customer name
    * display pricelist if it does'nt contain "catalogue in the name"

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>

Funders
-------

* GRAP, Groupement Régional Alimentaire de Proximité <http://www.grap.coop>
