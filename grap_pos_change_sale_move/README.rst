.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

======================================
Point Of Sale - Change Sale Move lines
======================================

this module intents to manage correctly sale move lines generated from
point of sale.

By default, with Odoo, account move lines are create by customer, even if
an invoices is not generated, and the date move is the date of the start of
the session. If a session is opened at the end of a year (or a month) and
closed in the next year (or month), it generates account errors (for years)
or analysis errors (for 

With this module, when closing a PoS session, an account move is created for
each combination of:

* day of orders.

In each account move

* a 'tax' line is created for each
    * VAT. (using pos_pricelist module)
* a 'product' line is created for each
    * products accounts
    * VAT
* a unique 'customer' line is created

This module should be used with grap_pos_change_payment_move.

This module overwrite the patch of pos_pricelist. (that is an overwrite too).

Credits
=======

Contributors
------------

* Sylvain LE GAL (https://twitter.com/legalsylvain)

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (www.grap.coop)
