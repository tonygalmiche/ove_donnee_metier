# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class ove_donnee_metier(osv.osv):
    _name = 'ove.donnee.metier'
    _description = u'Données métier de OVE'
    _rec_name = 'usager_id'
        
    _columns = {
        'usager_id': fields.many2one('is.dossier.usager', 'Usager', required=True),
        'date': fields.date('Date', required=True),
        'user_ids': fields.many2many('res.users', 'is_ove_user_doc_rel', 'doc_id', 'user_id', u'Rédacteurs'),
        'title': fields.char('Titre', required=True),
        'body': fields.html('Contenu', required=True),  
        'comment_ids': fields.one2many('is.ove.commentaires', 'doc_id', u'Professionnels ayant participé à la rédaction'),  
        'general_comment': fields.text(u'Commentaire général'),
        'attachment_ids': fields.many2many('ir.attachment', 'is_doc_attachment_rel', 'doc_id', 'attachment_id', 'Ajouter un nouveau fichier'),

        #'consult_group_id': fields.many2one('res.groups', u'Groupe ayant accès à la consultation du document'),
        #'modif_group_id': fields.many2one('res.groups', u'Groupe ayant accès à la modification du document'),

        'consult_group_id': fields.many2one('ove.groupe', u'Groupe ayant accès à la consultation du document'),
        'modif_group_id': fields.many2one('ove.groupe', u'Groupe ayant accès à la modification du document'),

        'consult_users': fields.many2many('res.users', 'is_ove_doc_consult_users_rel', 'doc_id', 'user_id', u'Utilisateurs ayant accès à la consultation du document'),
        'modif_users': fields.many2many('res.users', 'is_ove_doc_modif_users_rel', 'doc_id', 'user_id', u'Utilisateurs ayant accès à la modification du document'),
    }
    
    _defaults = {
        'date': fields.datetime.now,
    }
    
#    def get_item_id(self, cr, uid, item, context=None):
#        """
#            Retourner l'id de menu passé en paramètre
#        """
#        data_obj = self.pool.get('ir.model.data')
#        item_ids = data_obj.search(cr, uid, [('name','=',item)], context=context)          
#        if item_ids:
#            item_id = data_obj.browse(cr, uid, item_ids[0], context=context).res_id
#            return item_id
#    
#    def get_model_id(self, cr, uid, model, context=None):
#        """
#            Retourner l'id de model passé en paramètre
#        """
#        model_obj = self.pool.get('ir.model')
#        item_ids = model_obj.search(cr, uid, [('model','=',model)], context=context)          
#        if item_ids:
#            return item_ids[0]
        
    
#    def get_access_data(self, cr, uid, context=None):
#        """
#            Retourner les menus d'accès et les modèles d'accès
#        """    
#        menus = []
#        menus.append(self.get_item_id(cr, uid, 'menu_is_ove', context))
#        menus.append(self.get_item_id(cr, uid, 'menu_is_ove_donnee_metier', context))
#        menus.append(self.get_item_id(cr, uid, 'menu_action_ove_donnee_metier', context))
#        
#        models = []
#        #models.append(self.get_model_id(cr, uid, 'is.dossier.usager', context))
#        #models.append(self.get_model_id(cr, uid, 'res.users', context))
#        #models.append(self.get_model_id(cr, uid, 'ir.attachment', context))
#        #models.append(self.get_model_id(cr, uid, 'res.groups', context))
#        rule_model_id = self.get_model_id(cr, uid, 'ove.donnee.metier', context)
#        models.append(self.get_model_id(cr, uid, 'is.ove.commentaires', context))
#        models.append(rule_model_id)
#        
#        data = {'rule_model': rule_model_id,
#                'menus': menus,
#                'models': models}       
#        return data
        
  
#    def manip_dynamic_access_rules(self, cr, uid, group_id, data, data_access, context=None):
#        """ Créer / Modifier une nouvelle règle de lecture pour le groupe courant
#            Ajouter les menus nécessaire au groupe courant
#            Ajouter les models nécessaires au groupe courant
#        """
#        access_obj = self.pool.get('is_access_rules')
#        model_obj = self.pool.get('ir.model')    
#        
#        if not access_obj.exist_rule(cr, uid, group_id, data_access['rule_model'], data['perm_read'], data['perm_write'], data['perm_create'], data['perm_unlink'], context):
#            access_obj.create_new_rule(cr, uid, data['name'], data_access['rule_model'], data['domain'], group_id, data['perm_read'], data['perm_write'], data['perm_create'], data['perm_unlink'], context)
#        else:
#            access_obj.write_rule(cr, uid, group_id, data_access['rule_model'], data['doc_id'], data['perm_read'], data['perm_write'], data['perm_create'], data['perm_unlink'], True, False, context)
#        access_obj.add_menu(cr, uid, group_id, data_access['menus'], context)
#        
#        for model_id in data_access['models']:
#            access_model = model_obj.read(cr, uid, model_id, ['model'], context)
#            model = {
#                'model_id': model_id,
#                'perm_read': True,
#                'perm_write': True,
#                'perm_create': False,
#                'perm_unlink': False,
#                'name': access_model['model'],
#            }
#            access_obj.add_model_access(cr, uid, model, group_id, context)
#        
#        return True
#        
#    
#    def create(self, cr, uid, vals, context=None):
#        access_obj = self.pool.get('is_access_rules')
#        
#        new_id = super(ove_donnee_metier, self).create(cr, uid, vals, context)
#        """ Traiter les acces dynamique 
#        """
#        data_access = self.get_access_data(cr, uid, context)
#        document = self.browse(cr, uid, new_id, context)
#        data = { 
#                'perm_read': False,
#                'perm_write': False,
#                'perm_unlink': False,
#                'perm_create': False,
#                'doc_id': new_id,
#            }
#        
#        if document.consult_group_id:
#            name = u'règle1 ' + document.date + '(consultation)'
#            data.update({'name': name, 'domain': "[('id','in',[%s])]" % (new_id), 'perm_read': True, 'perm_write': False})
#            self.manip_dynamic_access_rules(cr, uid, document.consult_group_id.id, data, data_access, context)
#            
#            name = u'règle2 ' + document.date + '(consultation)'
#            data.update({'name': name, 'domain': "[('id','not in',[%s])]" % (new_id), 'perm_read': False, 'perm_write': True})
#            self.manip_dynamic_access_rules(cr, uid, document.consult_group_id.id, data, data_access, context)
#        
#        if document.modif_group_id:
#            name = u'règle ' + document.date + '(modification)'
#            data.update({'name': name, 'domain': "[('id','in',[%s])]" % (new_id), 'perm_read': True, 'perm_write': True})
#            self.manip_dynamic_access_rules(cr, uid, document.modif_group_id.id, data, data_access, context)
#        
#        if document.consult_users:
#            group_id = self.get_item_id(cr, uid, 'group_is_ove_consult_virtual_group', context)
#            user_ids = [user.id for user in document.consult_users]
#            access_obj.add_users(cr, uid, group_id, user_ids, context)
#            
#        if document.modif_users:
#            group_id = self.get_item_id(cr, uid, 'group_is_ove_modif_virtual_group', context)
#            user_ids = [user.id for user in document.modif_users]
#            access_obj.add_users(cr, uid, group_id, user_ids, context)
#            
#        return new_id
#    
#    def write(self, cr, uid, ids, vals, context=None):
#        access_obj = self.pool.get('is_access_rules')
#        
#        """ Traiter les acces dynamique 
#        """
#        if 'consult_group_id' in vals or 'modif_group_id' in vals or 'consult_users' in vals or 'modif_users' in vals:
#            data_access = self.get_access_data(cr, uid, context)
#            document = self.browse(cr, uid, ids[0], context)
#            data = { 
#                    'perm_read': False,
#                    'perm_write': False,
#                    'perm_unlink': False,
#                    'perm_create': False,
#                    'doc_id': ids[0],
#            }
#        
#            if 'consult_group_id' in vals and vals['consult_group_id']:
#                print 'consult_group_id *****', vals['consult_group_id']
#                if document.consult_group_id:
#                    """ Supprimer l'id du document des règles associés au groupe précédent """
#                    access_obj.write_rule(cr, uid, document.consult_group_id.id, data_access['rule_model'], ids[0], True, False, False, False, False, True, context)
#                    access_obj.write_rule(cr, uid, document.consult_group_id.id, data_access['rule_model'], ids[0], False, True, False, False, False, True, context)
#                    
#                name = u'règle1 ' + document.date + '(consultation)'
#                data.update({'name': name, 'domain': "[('id','in',[%s])]" % (ids[0]), 'perm_read': True, 'perm_write': False})
#                self.manip_dynamic_access_rules(cr, uid, vals['consult_group_id'], data, data_access, context)
#            
#                name = u'règle2 ' + document.date + '(consultation)'
#                data.update({'name': name, 'domain': "[('id','not in',[%s])]" % (ids[0]), 'perm_read': False, 'perm_write': True})
#                self.manip_dynamic_access_rules(cr, uid, vals['consult_group_id'], data, data_access, context)
#        
#            if 'modif_group_id' in vals and vals['modif_group_id']:
#                if document.modif_group_id:
#                    """ Supprimer l'id du document des règles associés au groupe précédent """
#                    access_obj.write_rule(cr, uid, document.modif_group_id.id, data_access['rule_model'], ids[0], True, True, False, False, False, True, context)

#                name = u'règle ' + document.date + '(modification)'
#                data.update({'name': name, 'domain': "[('id','in',[%s])]" % (ids[0]), 'perm_read': True, 'perm_write': True})
#                self.manip_dynamic_access_rules(cr, uid, vals['modif_group_id'], data, data_access, context)
#        
#            if 'consult_users' in vals and vals['consult_users']:
#                group_id = self.get_item_id(cr, uid, 'group_is_ove_consult_virtual_group', context)
#                access_obj.add_users(cr, uid, group_id, vals['consult_users'][0][2], context)
#            
#            if 'modif_users' in vals and vals['modif_users']:
#                group_id = self.get_item_id(cr, uid, 'group_is_ove_modif_virtual_group', context)
#                access_obj.add_users(cr, uid, group_id, vals['modif_users'][0][2], context)
#                
#        return super(ove_donnee_metier, self).write(cr, uid, ids, vals, context)
    

class is_ove_commentaires(osv.osv):
    _name = 'is.ove.commentaires'
    _description = 'Commentaires sur les documents'
    _rec_name = 'user_id'
    
    _columns = {
        'user_id': fields.many2one('res.users', 'Nom', required=True),
        'comment': fields.text('Commentaire'),
        'doc_id': fields.many2one('ove.donnee.metier', 'Document'),
    }
