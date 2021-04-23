# -*- coding: utf-8 -*-
{
    'name': 'CRM Diagnostic',
    'version': '0.1',
    'category': 'Crm',
    'summary': 'CRM Diagnostic',
    'description': """
CRM Diagnostic
==============
    """,
    'depends': [
        'base',
        'web',
        'crm',
        'crm_uni_forms',
        'base_user_role'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/web_assets.xml',
        'data/email_template.xml',
        'data/ir_cron.xml',
        'views/crm_lead_view.xml',
        'views/crm_diagnostic_view.xml',
        'views/inherit_base_user_role_view.xml',
        'views/crm_attention_plan_view.xml',
        'report/crm_diagnostic_report_template.xml',
        'report/crm_diagnostic_report.xml',
        'report/crm_attention_plan_template.xml',
        'report/crm_attention_plan_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}