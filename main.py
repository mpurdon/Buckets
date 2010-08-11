from bucket import BucketListHandler, ListItem
from google.appengine.api import memcache, users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from reset import ResetHandler
import os

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
            
        query = ListItem.all()
        query.order('-__key__')
        
        template_values = {
            'user': user.nickname(),
            'list_items': query.fetch(10),
            'url': users.create_logout_url(self.request.uri),
            'url_text': 'Log out',
            'memcache_stats': memcache.get_stats()
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))          

def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/view', BucketListHandler),
        ('/add', BucketListHandler),
        ('/reset', ResetHandler),
        ], debug=True)
        
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
