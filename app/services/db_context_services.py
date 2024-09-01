"""
This file contains the implementation of the DBContext class.
"""
from .kit_services import singleton



@singleton
class DBService:
    """
    This class is used to manage the database connections.
    """
    def __init__(self):
        self.db_service = DBService()

    def get_db_service(self):
        """
        This method returns the instance of the DBService class.
        """
        return self.db_service