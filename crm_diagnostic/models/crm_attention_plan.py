# -*- encoding: utf-8 -*-
from odoo import models, fields, api
from lxml import etree
import json


class CrmAttentionPlan(models.Model):
    _name = 'crm.attention.plan'
    _rec_name = 'nombre_negocio'


    nombre_negocio = fields.Char(
        string='Nombre del negocio'
    )
    ubicacion = fields.Char(
        string='Ubicación'
    )
    responsable = fields.Char(
        string='Responsable'
    )
    fecha = fields.Date(
        string='Fecha'
    )
    diagnostico = fields.Selection(
        selection=[
            ('competitividad', 'Nivel de competitividad'),
            ('incipiente', 'Incipiente'),
            ('aceptable', 'Aceptable'),
            ('confiable', 'Confiable'),
            ('competente', 'Competente'),
            ('excelencia', 'Excelencia')],
        string='Diagnostico'
    )
    #programa de entrenamiento
    programa = fields.Char(
        string='Programa'
    )
    duración = fields.Char(
        string='Duración (horas)'
    )
    inicia = fields.Char(
        string='Inicia'
    )
    finaliza = fields.Char(
        string='Finaliza'
    )
    plataforma = fields.Char(
        string='Plataforma'
    )
    enlace = fields.Char(
        string='Enlace para ingresar'
    )
    soluciones = fields.Text(
        string='Soluciones'
    )
    # cursos virtuales
    cvc_programa = fields.Char(
        string='Programa'
    )
    cvc_duración = fields.Char(
        string='Duración (horas)'
    )
    cvc_inicia = fields.Char(
        string='Inicia'
    )
    cvc_finaliza = fields.Char(
        string='Finaliza'
    )
    cvc_plataforma = fields.Char(
        string='Plataforma'
    )
    cvc_enlace = fields.Char(
        string='Enlace para ingresar'
    )
    cvc_soluciones = fields.Text(
        string='Soluciones'
    )
    #mentorias
    tema = fields.Char(
        string='Tema'
    )
    mentor = fields.Char(
        string='Mentor'
    )
    horario = fields.Char(
        string='Horario'
    )
    m_soluciones = fields.Text(
        string='Soluciones'
    )
    #indicadores
    indicador1 = fields.Char(
        string='Indicador 1'
    )
    indicador2 = fields.Char(
        string='Indicador 2'
    )
    #Lineas
    plan_line_ids = fields.One2many(
        'crm.attention.plan.line',
        'crm_attention_id'
    )
    lead_id = fields.Many2one(
        'crm.lead'
    )
    partner_id = fields.Many2one(
        'res.partner',
        related='lead_id.partner_id'
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda self : self.env.company)

    prioridad_related = fields.Char(related='plan_line_ids.prioridad')
    actividad_related = fields.Char(related='plan_line_ids.actividades')
    soluciones_related = fields.Char(related='plan_line_ids.soluciones')

    # validating if the current user has the facilitador profile
    def is_facilitator(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'facilitador')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    # validating if the current user has the cordinator profile
    def is_cordinator(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'coordinador')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    # validating if the current user has the mentor profile
    def is_mentor(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'mentor')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False
    
    def is_orientador(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'orientador')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    def is_admin(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'admin')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    def is_administrativo(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'administrativo')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    def is_estudiante(self):
        role_id = self.env['res.users.role'].sudo().search([('role_type', '=', 'estudiante')])
        for role in role_id:
            if any(user.id == self.env.user.id for user in role.line_ids.mapped('user_id')):
                return True
        return False

    @api.model
    def fields_view_get(
            self, view_id=None, view_type='form', toolbar=False,
            submenu=False):
        res = super(CrmAttentionPlan, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type == 'form':
            doc = etree.XML(res['arch'])

            if self.is_facilitator():
                for node in doc.xpath("//form"):
                    node.set("create", 'false')
                    node.set("edit", 'false')
            res['arch'] = etree.tostring(doc)

        if view_type == 'tree':
            doc = etree.XML(res['arch'])

            if self.is_facilitator():
                for node in doc.xpath("//tree"):
                    node.set("create", 'false')
            res['arch'] = etree.tostring(doc)

        return res

       
    def write(self, values, flag = False):
        lines = []
        lines_new = []
        unlink_lines = []
        priodidades = []
        actividades = []
        adjuntos = []
        contador = 0
        lead = self.env['crm.lead'].browse(self.lead_id.id)
        print(self.plan_line_ids)
        for l in lead.plan_line_ids:
            print(l.estado_actividad)
            if l.estado_actividad:
                print(l.estado_actividad)
                actividades.append(l.estado_actividad)
                adjuntos.append(l.adjunto)
                unlink_lines.append(l.id)
            else:
                actividades.append("pendiente_programar")
                unlink_lines.append(l.id)
        for item in self.plan_line_ids:
            print([item.prioridad, item.actividades, item.soluciones, item.reponsable, ])
            priodidades.append([item.prioridad, item.actividades, item.soluciones, item.reponsable, ])
        
        print(actividades)
        for prioridad in priodidades:
            if len(unlink_lines) == 0:
                lines_new.append((0, 0, {
                    'prioridad': prioridad[0],
                    'actividades': prioridad[1],
                    'soluciones': prioridad[2],
                    'reponsable': prioridad[3],
                    'estado_actividad': "pendiente_programar"
                }))
            else:
                lines.append(
                    (0, 0, {
                        'prioridad': prioridad[0],
                        'actividades': prioridad[1],
                        'soluciones': prioridad[2],
                        'reponsable': prioridad[3],
                        'estado_actividad': actividades[contador],
                        'adjunto' : adjuntos[contador]
                    }))
            contador += 1
        print(lines)
        for i in lead.plan_line_ids:
                i.unlink()
        if len(lines) == 0:
            lead.plan_line_ids = lines_new
        else:
            
            lead.plan_line_ids = lines
        #self.update_lead_plan_line(lead, lines)
        return super(CrmAttentionPlan, self).write(values), self.update_lead_plan_line(lead, lines)

    def update_lead_plan_line(self, lead, lines):
        for i in lead.plan_line_ids:
                i.unlink()
        print("teejecutas????????????????")
        lead.plan_line_ids = lines
        return 



class CrmAttentionPlanLines(models.Model):
    _name = 'crm.attention.plan.line'

    crm_attention_id = fields.Many2one(
        'crm.attention.plan'
    )
    crm_attention_id_1 = fields.Many2one(
        'crm.lead'
    )
    prioridad = fields.Char(
        string='Prioridad'
    )
    actividades = fields.Char(
        string='Actividades'
    )
    soluciones = fields.Char(
        string='Soluciones'
    )
    reponsable = fields.Char(
        string='Responsable'
    )
    
    estado_actividad = fields.Selection(
        [
            ('programada', 'Programada'),
            ('pendiente_programar', 'Pendiente a programar'),
            ('cancelada', 'Cancelada'),
            ('completada', 'Completada'),
            ('sin_actividad_relacionada', 'Sin actividad relacionada')
        ],
        default = "pendiente_programar"
    )
    adjunto = fields.Binary()



