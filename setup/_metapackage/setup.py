import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-grap-grap-odoo-custom",
    description="Meta package for grap-grap-odoo-custom Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-grap_change_access',
        'odoo12-addon-grap_change_data',
        'odoo12-addon-grap_change_email',
        'odoo12-addon-grap_change_precision',
        'odoo12-addon-grap_change_translation',
        'odoo12-addon-grap_change_views_base',
        'odoo12-addon-grap_change_views_product',
        'odoo12-addon-grap_change_views_stock',
        'odoo12-addon-grap_cooperative',
        'odoo12-addon-grap_theme',
        'odoo12-addon-server_environment_files',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
