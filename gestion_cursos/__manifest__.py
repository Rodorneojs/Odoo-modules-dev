# -*- coding: utf-8 -*-
{
    'name': "gestion_cursos",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Rodri",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/alumnos_views.xml',
        'views/clases_views.xml',
        'views/curso_views.xml',
        'views/evaluacion_views.xml', 
        'views/inscripcion_views.xml',  
        'views/docente_views.xml', 
        'views/wizard_inscripcion_views.xml',
        'reports/report.xml',
        'reports/reporte_lista_alumnos_template.xml',
        'views/menus.xml',   
        'views/templates.xml',
        'data/email_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

