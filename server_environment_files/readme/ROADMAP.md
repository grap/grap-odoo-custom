Create a `server_environment_files_pos` module,
once `pos_environment` module will be migrated in V18.0
and restore in that module the inheritance of this view.

```xml
<template id="point_of_sale_index" inherit_id="point_of_sale.index">
    <xpath expr="." position="inside">
        <t t-set="point_of_sale_index_path"
            t-value="request.env['ir.config_parameter'].sudo()
            .get_param('point_of_sale_index_path', None)" />
        <link t-if="point_of_sale_index_path"
            rel="stylesheet"
            t-att-href="point_of_sale_index_path"/>
    </xpath>
</template>
```
