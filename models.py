import db
import MySQLdb as mdb

class BaseModel(object):
  _table_name = ''

  def __init__(self, data = None):
    self.id = ''
    
    if data is not None:
      for k in data.keys():
        vars(self)[k] = data[k]

  @classmethod
  def find(cls, settings, id):
    cur = settings.dbconnection.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM " + cls._table_name + " WHERE ID = '" + str(id) + "'")
    data = cur.fetchone()
    return cls(data)

class Animal(BaseModel):
  _table_name = 'animal'
  
  def __init__(self, data = None):
    BaseModel.__init__(self, data)
    
    

class Client(BaseModel):
  aliases = {
      'names': 'ClientForenames',
      'surname': 'ClientSurname',
      }
  _table_name = 'client'

  def __setattr__(self, name, value):
      name = self.aliases.get(name, name)
      object.__setattr__(self, name, value)

  def __getattr__(self, name):
      if name == "aliases":
          raise AttributeError  # http://nedbatchelder.com/blog/201010/surprising_getattr_recursion.html
      name = self.aliases.get(name, name)
      return object.__getattribute__(self, name)

  def __init__(self, data = None):
    BaseModel.__init__(self, data)

  def to_label(self):
    return self.surname + ', ' + self.names

