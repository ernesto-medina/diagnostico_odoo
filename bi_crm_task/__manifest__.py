# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Create Task from Lead',
    'version': '13.0.0.1',
    'category': 'CRM',
    'summary': 'This odoo apps helps user to easily create new task with deadline and project name directly from lead.',
    'description': """
    Task on Lead, Add Task from lead, Task Lead, Create Project Task from Lead, Add task from mail, Create task from mail.Task on lead, add task on lead, tasks on lead, lead tasks, automated task by lead, Generate task from lead.
""",
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.in',
    'depends': ['base', 'crm', 'sale', 'project'], # timesheet_grid
    'data': [ 
             'views/crm_lead_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "images":['static/description/Banner.png'],
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
