# -*- coding: utf-8 -*-
{
    "name": """Website Page Version""",
    "summary": """Allow to save all versions of your website page.""",
    "category": "Website",
    "images": [],
    "version": "9.0.1.0.0",
    "application": False,

    "author": "Dinar Gabbasov",
    "website": "https://twitter.com/gabbasov_dinar",
    "license": "LGPL-3",

    "depends": [
        "website",
    ],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
        "security/ir.model.access.csv",
        "views/website_version_templates.xml",
        "views/marketing_view.xml",
    ],
    "qweb": [
        "static/src/xml/*.xml",
    ],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
