# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class is_access_rules(osv.osv):
    _name = 'is_access_rules'
    _description = u'accès dynamiques'  
    
    def exist_access_model(self, cr, uid, model_id, group_id, context=None):
        """
        exist access_model dans le groupe
        """
        access_model_obj = self.pool.get('ir.model.access')
        ids = access_model_obj.search(cr, uid, [('model_id','=',model_id),('group_id','=',group_id)], context=context)
        if ids:
            return True
        return False       
    
    
    def exist_rule(self, cr, uid, group_id, model_id, perm_read, perm_write, perm_create, perm_unlink, context=None):
        """
        exist rule
        """
        rule_obj = self.pool.get('ir.rule')
        rule_ids = rule_obj.search(cr, uid, [('groups','in', [id for id in [group_id]]),
                                             ('model_id','=',model_id),
                                             ('perm_read','=',perm_read),
                                             ('perm_write','=',perm_write),
                                             ('perm_create','=',perm_create),
                                             ('perm_unlink','=',perm_unlink),], context=context)
        if rule_ids:
            return rule_ids
        return False
    
    def transform_domain(self,cr, uid, force_domain, doc_id, add, unlink, context=None):
        """
        Mettre à jour le domaine:
        - si add = True, Ajouter doc_id au domaine
        - si unlink = True, Supprimer doc_id du domaine
        """ 
        domain = False
        if add:           
            domain = str(force_domain)[0:len(force_domain)-3] + ',' + str(doc_id) + '])]'
        if unlink:
            if force_domain.count(',' + str(doc_id)) > 0:
                domain = force_domain.replace(',' + str(doc_id),'')
        print 'domain ******', domain
        return domain
    
    
    def create_new_rule(self, cr, uid, name, model_id, domain, group_id, perm_read, perm_write, perm_create, perm_unlink, context=None):
        """
        Create a rule
        """
        rule_obj = self.pool.get('ir.rule')
        vals = {
            'name': name,
            'model_id': model_id,
            'perm_read': perm_read,
            'perm_write': perm_write,
            'perm_create': perm_create,
            'perm_unlink': perm_unlink,
            'domain_force': domain,
            'groups': [(6, 0, [group_id])],
        }
        new_id = rule_obj.create(cr, uid, vals, context=context)
        return new_id
    
    
    def write_rule(self, cr, uid, group_id, model_id, doc_id, perm_read, perm_write, perm_create, perm_unlink, add, unlink, context=None):
        """
        Update rule:
        - si add = True, Ajouter le doc_id dans le domaine
        - si add = False, Supprimer le doc_id de domaine
        """
        rule_obj = self.pool.get('ir.rule')
        rule_ids = self.exist_rule(cr, uid, group_id, model_id, perm_read, perm_write, perm_create, perm_unlink, context)
        if rule_ids:
            rule = rule_obj.read(cr, uid, rule_ids[0], ['domain_force'], context)         
            domain = self.transform_domain(cr, uid, rule['domain_force'], doc_id, add, unlink, context)
            if domain:
                rule_obj.write(cr, uid, rule_ids[0], {'domain_force': domain}, context)
            else:
                """ Supprimer la règle courante """
                rule_obj.unlink(cr, uid, rule_ids, context) 
        return True
    
    def add_users(self, cr, uid, group_id, users, context=None):
        """
        Ajouter des utilisateurs dans le groupe
        """
        group_obj = self.pool.get('res.groups')
        group = group_obj.read(cr, uid, group_id, ['users'], context)
        user_ids = group['users']
        print 'user_ids ****', user_ids
        print 'users ****', users
        for user in users:
            print 'user ******', user
            if user not in user_ids:
                print 'user in user_ids ****', user
                user_ids.append(user)
        print 'user_ids after add ****', user_ids               


        # Relation many2many en bas de cette page : https://doc.odoo.com/v6.0/developer/2_5_Objects_Fields_Methods/methods.html/
        group_obj.write(cr, uid, group_id, {'users': [(6, 0, user_ids)]}, context)
        return True
        
    def add_menu(self, cr, uid, group_id, menus, context=None):
        """
        Ajouter des menus dans le groupe
        """
        group_obj = self.pool.get('res.groups')
        group = group_obj.read(cr, uid, group_id, ['menu_access'], context)
        menu_ids = group['menu_access']
        for menu in menus:
            if menu not in menu_ids:
                menu_ids.append(menu) 
        group_obj.write(cr, uid, group_id, {'menu_access': [(6, 0, menu_ids)]}, context)
        return True
    
    
    def add_model_access(self, cr, uid, model, group_id, context=None):
        """
        Ajouter les model_access
        """
        if not self.exist_access_model(cr, uid, model['model_id'], group_id, context):
            access_model_obj = self.pool.get('ir.model.access')
            vals = {
                'model_id': model['model_id'],
                'perm_read': model['perm_read'],
                'perm_write': model['perm_write'],
                'perm_create': model['perm_create'],
                'perm_unlink': model['perm_unlink'],
                'name': model['name'],
                'group_id': group_id,
            }
            access_model_obj.create(cr, uid, vals, context)
        return True       
        
        
        
