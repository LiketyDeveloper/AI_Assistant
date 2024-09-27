import peewee as pw
from . import main


database = main.handler


class BaseModel(pw.Model):
    class Meta:
        database = database


class Operators(BaseModel):
    user_id = pw.BigIntegerField(column_name="user_id", primary_key=True)
    username = pw.CharField(column_name="username", max_length=128)
    working = pw.BooleanField(column_name="working")
    
    class Meta:
        table_name = 'Operators'
        
        
class Users(BaseModel):
    user_id = pw.BigIntegerField(column_name="user_id", primary_key=True)
    username = pw.CharField(column_name="username", max_length=128)
    history = pw.TextField(column_name="history")  
    handled_by = pw.BigIntegerField(column_name="handled_by") ## 0 means the user is not being supported
    
    class Meta:
        table_name = 'Users'
        
        
def register_models(model_classes: BaseModel):
    database.create_tables(model_classes)
    