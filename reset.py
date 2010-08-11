from bucket import BucketListHandler, ListItem
from google.appengine.api import memcache, users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from models import Person, Place, Thing, UserListItems, UserListItem, ListItemCounter
import datetime
import os

class ResetHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        
        # Delete all list items
        self.response.out.write('<hr/>Deleting All Items<hr/>')
        all_items = ListItem.all()
        self.response.out.write('Deleting %d items<br/>' % all_items.count())
        for item in all_items:
            self.response.out.write('Deleted %s<br/>' % item)
            item.delete()
            
        # Delete all User Lists
        self.response.out.write('<hr/>Deleting All User Lists<hr/>')
        all_items = UserListItems.all()
        self.response.out.write('<hr/>Deleting %d user lists<hr/>' % all_items.count())
        for item in all_items:
            self.response.out.write('Deleted list for %s<br/>' % item.user)
            item.delete()

        self.add_people(user)
        self.add_places(user)
        self.add_things(user)

        self.response.out.write('<hr/>Flushing memcached<hr/>')
        
        # Flush memcache
        memcache.flush_all()
        
        self.response.out.write('<hr/>All Records<hr/>')
        for item in ListItem.all():
            self.response.out.write('%s<br/>' % item)

        self.response.out.write('<br/><a href="/">Back to home page...</a>')

    def add_people(self, user):
        # Add 10 People
        people = [
            'Nelson Mandella',
            'the Queen of England',
            'the Pope',
            'President Obama',
            'Richard Branson',
            'Bill Gates',
            'Warren Buffet',
            'Bon Jovi',
            'Jennifer Aniston'
        ]
        
        self.response.out.write('<hr/>Adding people to meet<hr/>')

        # Get all list items for the current user        
        query = UserListItems.gql('WHERE user = :user', user=user)
        user_list_items = query.get()
        
        if user_list_items is None:
            user_list_items = UserListItems(user=user)

        for name in people:
            # Add Person Entity
            person = Person()
            person.title = name
            person.put()
            
            # Add Reference to the Person from User
            user_list_item = UserListItem()
            user_list_item.user = user
            user_list_item.list_item = person
            
            # Update the list of items the user has
            user_list_items.list_items.append(person.key())
            
            # Add the specifics of the user list item linkage
            user_list_item = UserListItem()
            user_list_item.user = user
            user_list_item.list_item = person
            one_year = datetime.timedelta(days=365)
            today = datetime.datetime.today()
            user_list_item.date_due = today + one_year
            user_list_item.put()
            
            ListItemCounter.increment(user_list_item)
            
            self.response.out.write('Added %s<br/>' % person)

        # Save the linkages from list items to the current user
        user_list_items.put();

    def add_places(self, user):
    
        # Add 10 Places
        places = [
            'the CN Tower',
            'the Eiffel Tower',
            'Athens Greece',
            'the Great Pyramids',
            'the Great Wall of China',
            'the Louvre',
            'the Palace of Versailles',
            'Sydney Australia',
            'the Grand Canyon',
            'Bora Bora'
        ]
        
        self.response.out.write('<hr/>Adding places to go<hr/>')
        
        # Get all list items for the current user        
        query = UserListItems.gql('WHERE user = :user', user=user)
        user_list_items = query.get()
        
        if user_list_items is None:
            user_list_items = UserListItems(user=user)        
        
        for name in places:
            place = Place()
            place.title = name
            place.put()
            
            # Add Reference to the Place from User
            user_list_item = UserListItem()
            user_list_item.user = user
            user_list_item.list_item = place
            
            # Update the list of items the user has
            user_list_items.list_items.append(place.key())
            
            # Add the specifics of the user list item linkage
            user_list_item = UserListItem()
            user_list_item.user = user
            user_list_item.list_item = place
            one_year = datetime.timedelta(days=365)
            today = datetime.datetime.today()
            user_list_item.date_due = today + one_year
            user_list_item.put()            

            self.response.out.write('Added %s<br/>' % place)

    def add_things(self, user):

        # Add 10 Things
        things = [
            'read War and Peace',
            'sky dive',
            'learn to SCUBA dive',
            'get a university degree',
            'learn to sail',
            'learn to kite board',
            'learn to play guitar',
            'learn archery',
            'learn spanish',
            'learn chinese',
        ]
        
        self.response.out.write('<hr/>Adding things to do<hr/>')
        
        # Get all list items for the current user        
        query = UserListItems.gql('WHERE user = :user', user=user)
        user_list_items = query.get()

        if user_list_items is None:
            user_list_items = UserListItems(user=user)        
        
        for name in things:
            thing = Thing()
            thing.title = name
            thing.put()
            
            # Add Reference to the Thing from User
            user_list_item = UserListItem()
            user_list_item.user = user
            user_list_item.list_item = thing
            
            # Update the list of items the user has
            user_list_items.list_items.append(thing.key())
            
            # Add the specifics of the user list item linkage
            user_list_item = UserListItem()
            user_list_item.user = user
            user_list_item.list_item = thing
            one_year = datetime.timedelta(days=365)
            today = datetime.datetime.today()
            user_list_item.date_due = today + one_year
            user_list_item.put()            
            
            self.response.out.write('Added %s<br/>' % thing)
