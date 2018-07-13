.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================
GRAP - Change Ir Values
=======================

Set ir.values for default feature

Email composition wizard (mail.compose.message)
-----------------------------------------------

* Purchase Email is based on purchase order template (and not RFC)
    * field: template_id
    * value: ref('purchase.email_template_edi_purchase_done')

Products (product.template)
---------------------------

* Products has Null Produce Delay
    * field: produce_delay
    * value: 0
* Products has Null Sale Delay
    * field: sale_delay
    * value: 0

Credits
=======

Contributors
------------

* Julien WESTE
* Sylvain LE GAL <https://twitter.com/legalsylvain>

Funders
-------

* GRAP, Groupement Régional Alimentaire de Proximité <http://www.grap.coop>
