# -*- coding: utf-8 -*-

{
    'name': 'OVE - Données Métier',
    'version': '1.0',
    'category': 'InfoSaône',
    'description': """
Données Métier de OVE
""",
    'author': 'Tony GALMICHE / Asma BOUSSELMI',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': ['base', 'is_ove'],
    'data': ['security/is_ove_security.xml',
             #'security/ir.model.access.csv',
             'ove_donnee_metier_view.xml',
             'is_access_data.xml'
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
