"""
Test    app/utils/databases.p.py
Author: Firstname Lastname
Date:   2022/11/29  10:00 AM
"""

import unittest

from sqlalchemy.orm import sessionmaker

from app.utils.databases import (
    check_database_exist ,
    create_database,
    get_all_tables,switch_database,
    get_all_columns_of_table,
    get_all_columns_of_model,
)
from app.models.users import User

class TestAppUtilsDatabases(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAppUtilsDatabases, self).__init__(*args, **kwargs)
        self.engine = None
        self.session = None

    def setUp(self):
        """
        This method is called before each test function.
        :return:
        """
        # connect to mysql database
        from sqlalchemy import create_engine
        self.engine = create_engine('mysql+pymysql://root:123456@localhost:3306')
        self.session = sessionmaker(bind=self.engine)()


    def test_check_database_exist(self):
        """
        Test check_database_exist function
        :return:
        """
        # check if database exist
        self.assertFalse(check_database_exist(self.session, 'test'))

        # check if database does not exist
        self.assertFalse(check_database_exist(self.session, 'test_db_not_exist'))

    def test_create_database(self):
        """
        Test create_database function
        :return:
        """
        # create database

        self.assertTrue(create_database(self.session, 'test'))
        # check if database exist
        # self.assertTrue(create_database(self.session, 'test_db_not_exist'))
    def test_get_all_tables(self):
        """
        Test get_all_tables function
        :return:
        """
        # get all tables

        tables=get_all_tables(self.session,'test')
        print(tables)
        self.assertIsNotNone(tables)
    def test_get_all_columns_of_table(self):
        """
        Test get_all_columns_of_table function
        :return:
        """
        # get all columns of table

        columns=get_all_columns_of_table(self.session,'test','users')
        print(columns)
    def test_get_all_columns_of_model(self):
        """
        Test get_all_columns_of_model function
        :return:
        """
        # get all columns of model

        columns=get_all_columns_of_model(Users)
        print(columns)

    def test_switch_database(self):
        """
        Test switch_database function
        :return:
        """
        # switch database

        self.assertTrue(switch_database(self.session, 'test'))
        # check if database exist
        # self.assertTrue(switch_database(self.session, 'test_db_not_exist'))





if __name__ == '__main__':
    unittest.main()
