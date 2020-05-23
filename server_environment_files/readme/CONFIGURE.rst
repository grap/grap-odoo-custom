Open your ``odoo.cfg`` file and add the following lines, replacing ``RUNNING_ENV``
value by the one the values : ``dev``, ``test``, ``production`` or ``spare``.

.. code-block::

    [options]
    running_env = RUNNING_ENV

    [ir.config_parameter]
    web_login_layout_path = /server_environment_files/static/RUNNING_ENV/web_login_layout.css
    web_webclient_bootstrap_path = /server_environment_files/static/RUNNING_ENV/web_webclient_bootstrap.css
    point_of_sale_index_path = /server_environment_files/static/RUNNING_ENV/point_of_sale_index.css
