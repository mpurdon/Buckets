from google.appengine.api import memcache, users
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from models import ListItem, UserListItems
import logging
import os

class BucketListHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template_content = self.render_list_items(user)
        self.response.out.write(template_content)        

    def post(self):
        user = users.get_current_user()
        
        # We require a valid user
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
    
        list_item = ListItem()
        
        list_item.author = user
        list_item.title = self.request.get('title')
        list_item.details = self.request.get('details')

        # If we were able to save, get rid of the template cache
        if list_item.put():
            memcache_key = user.nickname() +  '_list_items'            
            memcache.delete(memcache_key)

        self.redirect('/view')
        
    def render_list_items(self, user):

        memcache_key = user.nickname() +  '_list_items'        
        template_content = memcache.get(memcache_key)
        
        if template_content is not None:
            return template_content

        query = UserListItems.gql('WHERE user = :user', user=user)
        user_list_items = query.get()
        
        # Use multi-get to pull all list items for this user
        list_items = ListItem.get(user_list_items.list_items)
        
        template_values = {
            'user': user.nickname(),
            'list_items': list_items,
            'view_javascript': 'view'
        }
        path = os.path.join(os.path.dirname(__file__), 'view.html')
        template_content = template.render(path, template_values)
        
        if not memcache.add(memcache_key, template_content):
            logging.error('Memcache: Could not set ' + memcache_key)
            
        return template_content                    
