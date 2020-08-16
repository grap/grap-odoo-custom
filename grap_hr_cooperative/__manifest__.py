{
    "name": "HR Grap Cooperative Custom",
    "summary": """
        Customization specific to GRAP  : Link with Cooperative module.
    """,
    "license": "AGPL-3",
    "author": "GRAP",
    "website": "http://www.grap.coop",
    "category": "Human Resources",
    "version": "12.0.0.2.0",
    "depends": ["grap_cooperative", "hr_cae"],
    "data": [
        "views/grap_activity.xml",
        "views/grap_people.xml",
        "views/hr_employee.xml"
    ],
    "demo": [],
    "installable": True,
}
