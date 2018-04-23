.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==========================
GRAP Custom - Change Email
==========================

This module extends the functionality of mail and email_template module to
changes default email templates that doesn't fit with GRAP needs.

Technical Changes
=================

* add new ```active``` field on ```email.template``` model

* Change default_get on ```mail.compose.message``` and set ```template_id```
  field as required.

email templates
===============

* Disable 

Contributors
------------

* Sylvain LE GAL (https://www.twitter.com/legalsylvain)

Do not contact contributors directly about support or help with technical issues.

Funders
-------

The development of this module has been financially supported by:

* GRAP, Groupement Régional Alimentaire de Proximité (http://www.grap.coop)
