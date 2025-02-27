Adds a PDF report to print BoM(s) in a very simple way.

.. figure:: ../static/description/food_menu_simple_report_new_action.jpeg

.. figure:: ../static/description/food_menu_simple_report_new_report.png

Compatible with [mrp.food.menu_widget_section_and_note_one2many](https://github.com/OCA/manufacture/tree/16.0/mrp.food.menu_widget_section_and_note_one2many)

Also compatible for being called in parent template. For this purpose, you need
to set params with t-set :
t-set="docs" → BoM
t-set="food_menu_intermediate_parent_food_menu_text" → nested BoM could be printed
t-set="food_menu_qty" → desired BoM quantity

Call this template with t-foreach to print multiple BoM with multiple BoM quantity
→ Example in grap-odoo-custom module : mrp.food.menu_wizard_production