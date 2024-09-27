import json
from loguru import logger

from bot.database.models import Users, Operators


class BaseUser:

    def __init__(self, user_id: int) -> None:
        self.is_operator = Operators.select().where(Operators.user_id == user_id).exists()
        self._user = Operators.get_or_none(user_id=user_id) if self.is_operator else Users.get_or_none(user_id=user_id)
        
        if self.is_operator:
            self.__class__ = Operator
            Operator.__init__(self, user_id)
        else:
            self.__class__ = User
            User.__init__(self, user_id)             


    def delete(self):
        try:
            self._user.delete_instance() 
            logger.info(f"Removed user {self.username} ID: {self.user_id}")
        except Exception as e:
            logger.error(f"Error while removing user {self.user_id}: {str(e)}")   


class User(BaseUser):


    def __init__(self, user_id: int, username: str = None, record: dict = None) -> None:
        self._user = Users.get_or_none(user_id=user_id)

        if not self._user:
            logger.info("Creating new user")
            self._user = Users.create(user_id=user_id, username=username if username else "", 
                                        history=f"{[record]}" if record else "[]", 
                                        handled_by=0)
            
            logger.info(f"Created new user {self._user.username} ID: {self.user_id}")          
                
        logger.info(f"Got user {self.username} ID: {self.user_id} from database")   
    
    
    @property
    def user_id(self) -> int:
        return self._user.user_id


    @property
    def username(self) -> str:  
        return self._user.username
    
    
    @username.setter
    def username(self, new_username: str):
        if not isinstance(new_username, str):
            raise ValueError("Username must be a string")
        
        self._user.username = new_username
        self._user.save()
        logger.info("Name was specified for the user") 


    @property
    def history(self) -> list:
        return json.loads(self._user.history)
    
    def __iadd__(self, record):        
        if not isinstance(record, str):
            raise ValueError("Record must be a string")
        
        try:
            history = json.loads(self._user.history)
            history.append(record)
            self._user.history = json.dumps(history, ensure_ascii=False)
            self._user.save()
            
            logger.info(f"Record was successfully added to user {self.username}'s history")
        except Exception as e:
            logger.error(f"Error while adding record to user {self.username}'s history: {str(e)}")
        
        
        return self


    @property
    def handled_by(self) -> int:
        return self._user.handled_by


    @handled_by.setter
    def handled_by(self, new_value: int) -> None:
        if not isinstance(new_value, int):
            raise TypeError("Handled_by value must be an integer")
        if not 0 <= new_value:
            raise ValueError("Handled_by must be a positive integer")
                
        self._user.handled_by = new_value
        self._user.save()
        

    @classmethod
    def list_users_needing_support(cls) -> list:
        """Returns a list of User instances that need support, i.e. for whom handled_by is 0."""

        return [
            cls(user_id=user.user_id) 
            for user in Users.select(Users.user_id).where(Users.handled_by == 0)
        ]

class Operator(BaseUser):
    

    def __init__(self, user_id: int, username: str = None) -> None:
        self._user = Operators.get_or_none(user_id=user_id)
        
        if not self._user:
            if not username:
                raise ValueError(f"Operator does not exist, to create operator you have to specify username")
            else:
                self._user = Operators.create(user_id=user_id, username=username, working=False)
                logger.success(f"Created new operator {username} ID: {self.user_id}")

        else:
            logger.info(f"Got operator {self.username} ID: {self.user_id} from database")


    @property
    def user_id(self) -> int:
        return self._user.user_id
    

    @property
    def username(self) -> str:  
        return self._user.username
    
    
    @property
    def working(self) -> int:
        return self._user.working


    @working.setter
    def working(self, new_working: bool) -> None:
        if not isinstance(new_working, bool):
            raise TypeError("Working status value must be a boolean")

        self._user.working = new_working
        self._user.save()
        logger.info(f"Operator {self.username} ID: {self.user_id} is {'working' if new_working else 'not working'}")
    

    @property
    def is_availiable(self) -> bool:
        return not self.is_busy and self.working

    
    @property
    def is_busy(self) -> bool:
        return bool(self.operator_assigned_user)


    @property
    def operator_assigned_user(self) -> User:
        """Get the user that the operator is currently assigned to

        Returns:
            User: The user that the operator is currently assigned to, or None if no such user exists
        """
        user = Users.get_or_none(Users.handled_by == self.user_id)
        
        return User(user_id=user.user_id) if user else None

    @property
    def free_operator():
        """Get an operator that is not busy and is available to support users
        
        Returns:
            Operator: An operator that is available to support users, or None if no such operator exists
        """
        try:
            result = [
                Operator(user_id=user.user_id)
                for user in Operators.select(Operators.user_id) 
                if Operator(user_id=user.user_id).is_availiable
            ][0]
        except IndexError:
            result = None
            
        return result   
                
        
    def connect_to(self, user_to_support: User) -> User:
        """Connect the operator to the given user, given that the user is not already being supported by another operator

        Args:
            user_to_support (User): The user to connect to

        Returns:
            User: The user that the operator is now connected to

        Raises:
            ValueError: If the user is already being supported by another operator
        """
        
        if user_to_support.handled_by != 0:
            raise ValueError(f"User {user_to_support.username} ID: {user_to_support.user_id} is already being supported by another operator")
        
        user_to_support.handled_by = self.user_id
        
        logger.info(f"Operator {self.username} ID: {self.user_id} is connected to user {user_to_support.username} ID: {user_to_support.user_id}")


