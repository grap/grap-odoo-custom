This module is a patch module, that overwrite the function ``_inverse_set_process_qty``
of the model ``product.product`` of the module ``base_product_mass_addition``.

It avoid to call the function ``odoo.tests.Form`` that is very slow, and that is making
the module ``purchase_quick`` unusable.


**Benchmark on a Production database, run locally**
Without this module, for a purchase, calling ``_inverse_set_process_qty`` takes
- 12.469824 seconds (for a create)
- 13.837742 seconds (for an update)

With this module, the same call takes
- 0.121779 seconds (for a create)
- 0.110520 seconds (for an update)


**Benchmark on a Demo database, run locally**

Test Code show that time is divided by 12.

.. code-block:: python

    import timeit
    def test():
        orders = env["purchase.order"].search([("partner_id", "=", env.ref("base.res_partner_1").id)])
        for line in orders.mapped("order_line"):
            product = line.product_id.with_context(parent_model="purchase.order", parent_id=line.order_id.id)
            product.qty_to_process = line.product_qty * 2


Without this module :

.. code-block:: python

    >>> timeit.timeit(test, number=50)
    70.18318000599902

With this module :

.. code-block:: python

    >>> timeit.timeit(test, number=50)
    5.822203948999231
