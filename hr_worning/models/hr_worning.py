# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

#from xmlrpc import client as xmlrpclib
import urllib.parse
from odoo.exceptions import UserError, AccessError

import xmlrpc.client
import requests
import json
from json import JSONEncoder



class HrWarning(models.Model):
    _name ='hr.worning'


    date = fields.Date(string = "Date")
    employee_id = fields.Many2one('hr.employee',string="Name")
    name_worning = fields.Many2one('hr.worning.conf', string = "Warning Type")
    reason = fields.Char(string="reason")

    punishment_type = fields.Selection([('dismiss','Dismiss'),('deduction','Deduction')])
    deduction_amount = fields.Float(string ="Amount")
    state = fields.Selection([('draft','Draft'),('done_worning','Done Punishment'),('cancel','Cancel')],default='draft')
    seq = fields.Many2one('ir.sequence',string="seq")
    max_boolean = fields.Boolean (string = "Boolean", default=False) 
   
    @api.multi
    def action_cancel(self):
        return self.write({'state': 'cancel'})
        
    @api.model
    def create(self, values):
        obj = self.env['hr.worning']
        record = super(HrWarning, self).create(values)

        count_worning =  obj.search_count([('employee_id','=',record['employee_id'].id),('state','!=','done_worning'),('state','!=','cancel'),('name_worning.name','=',record['name_worning'].name)])
        if count_worning == record['name_worning'].Max_number_worning :
            record['max_boolean'] = True    

        return record
           
    @api.multi     
    def action_Warning(self): 
        for data in self:
            contract_obj = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id)])
            if self.max_boolean == True:
                if self.punishment_type == 'dismiss':
                    self.employee_id.active = False 
                    for cont_employee in contract_obj:
                        cont_employee.state = 'close'   
                    worning_all_obj = self.env['hr.worning'].search([('employee_id', '=', self.employee_id.id)])              
                    worning_all_obj.write({'state': 'done_worning'})
                   
    @api.multi
    def unlink(self):
        for obj in self:
            if obj.state not in ('draft', 'cancel'):
                raise UserError(_('You cannot delete an Worning which is not draft or cancelled.'))
            
        return super(HrWarning, self).unlink()
               
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
       
               
    def get_inputs(self, contract_ids, date_from, date_to):
        """This Compute the other inputs to employee payslip.
                           """
        res = super(HrPayslip, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        emp_id = contract_obj.browse(contract_ids.id).employee_id
        worning_obj = self.env['hr.worning'].search([('employee_id', '=', emp_id.id), ('punishment_type', '=', 'deduction')])
        for worn in worning_obj:
                if date_from <= worn.date <= date_to and worn.punishment_type == 'deduction':

                    
                    for result in res:
                        if result.get('code') == 'WO':
                            result['amount'] = worn.deduction_amount
                            worning_all_obj = self.env['hr.worning'].search([('employee_id', '=', emp_id.id)])
                            worning_all_obj.write({'state': 'done_worning'})
        return res
        
class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    def _get_partner_id(self, credit_account):
        """
        Get partner_id of slip line to use in account_move_line
        """
        # use partner of salary rule or fallback on employee's address
        register_partner_id = self.salary_rule_id.register_id.partner_id
        partner_id = register_partner_id.id or self.slip_id.employee_id.address_home_id.id
        if credit_account:

            return partner_id
        else:

            return partner_id
        return False
                   

class WarningConfg(models.Model):
    _name ='hr.worning.conf'

    name = fields.Char(string= "Name")
    Max_number_worning = fields.Integer("Warning Numbers")
    

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.one
    def _compute_employee_Warning(self):
        """This compute theand total worning count of an employee.
            """
        self.number_of_worning =  self.env['hr.worning'].search_count([('employee_id','=',self.id)])

    number_of_worning = fields.Integer("Warning Numbers", compute='_compute_employee_Warning')





