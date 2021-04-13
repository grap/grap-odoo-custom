**Changes for ``point_of_sale`` modules**

* more info in ``pos.category`` form view.

* change the colors of the ``pos.order`` tree view (danger and warning for low margins).
* add default filter for ``pos.order`` tree view.

* change groups rules for ``account.bank.statement`` and ``account.bank.statement.line``.

**Create new view**

* "Point of sale > Order Lines"


**Alter module Pos Cash Move Reason**

* Statement lines (of cash moves) has now the date of the close of the session, if it
  is in a closing state. (Today otherwise)
