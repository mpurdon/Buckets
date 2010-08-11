from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class ListItem(polymodel.PolyModel):
    title = db.StringProperty()
    details = db.StringProperty(multiline=True)
    
    def top_ten(self):
        """
        Return the top ten items of this type
        """
        
        query = ListItem.all();
        query.order('-count')
        if self.class_name() is not 'ListItem':
            query.filter('class=%s' % self.class_name())
        
        
        return self.all().fetch(10)

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u'%s' % self.title

class Person(ListItem):
    def __unicode__(self):
        return u'meet %s' % self.title    

class Place(ListItem):
    location = db.GeoPtProperty()
    
    def __unicode__(self):
        return u'go to %s' % self.title    

class Thing(ListItem):
    def __unicode__(self):
        return u'%s' % self.title    

class ListItemCounter(db.Model):
    list_item = db.ReferenceProperty(ListItem)
    count = db.IntegerProperty(required=True, default=0)
    
    @staticmethod
    def increment(list_item):
        """
        """
        def tx():
            query = ListItemCounter.gql('WHERE list_item = :list_item', list_item=list_item)
            list_item_counter = query.get();
            
            if list_item_counter is None:
                list_item_counter = ListItemCounter(list_item=list_item)
                
            list_item_counter.count += 1
            list_item_counter.put() 

        db.run_in_transaction(tx)
            
    
class UserListItems(db.Model):
    user = db.UserProperty()
    list_items = db.ListProperty(db.Key)
    
class UserListItem(db.Model):
    list_item = db.ReferenceProperty(ListItem)
    date_added = db.DateTimeProperty(auto_now_add=True)
    date_due = db.DateTimeProperty()
    date_accomplished = db.DateTimeProperty()

    