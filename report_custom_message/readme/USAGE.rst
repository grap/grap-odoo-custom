* Add a report inheritance in your custom module

For example : 

```
<odoo>

    <template id="template_account_invoice" inherit_id="account.report_invoice_document" priority="1000">

        <xpath expr="//div[hasclass('page')]/h2/.." position="before">
            <t t-out="o.report_custom_message"/>
        </xpath>

    </template>

</odoo>

```

Or

```
<odoo>

    <template id="template_purchaseorder" inherit_id="purchase.report_purchaseorder_document" priority="1000">

        <xpath expr="//div[hasclass('oe_structure')]" position="after">
            <t t-out="o.report_custom_message"/>
        </xpath>

    </template>

</odoo>
```
