import os
import unittest
from dbconn import Database
from event import Event
from dbconn import ConnectionPool
from flask_bcrypt import Bcrypt
from flask import Flask


Database.initialise()
app = Flask(__name__)

class EventTest(unittest.TestCase):

    def setUp(self):
        bcrypt = Bcrypt(app)
        hashed_pass = bcrypt.generate_password_hash("1234567890").decode('utf-8')
        with ConnectionPool() as cursor:
            cursor.execute("INSERT INTO user_info(firstname, lastname, username, email, passwrd, institution, usertype)"
                           "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                           ("test_name", "test_sur", "testusername", "test@test.com", hashed_pass, "test_institution", "University Representative"))

            cursor.execute("SELECT userid FROM user_info where username = 'testusername'")
            test_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO institution_info(institutionName, webAdress, info, contactInfo, representativeId, isRegistered) "
                       "VALUES(%s,%s,%s,%s,%s,%s)" , ("NEW INSTITUTION" , "new.new.com", "new information", "0000",test_id , True))

            cursor.execute("SELECT institutionID FROM institution_info where webAdress = 'new.new.com'")

            self.hostID = cursor.fetchone()[0]


    def tearDown(self):
        with ConnectionPool() as cursor:
            cursor.execute("Delete from user_info where username = 'testusername'")
            cursor.execute("Delete from institution_info where webAdress = 'new.new.com'")
            cursor.execute("Delete from event_info where hostID = %s" , (self.hostID,))

    def insert_check(self, event):
        test_event_id = event.save_to_db()
        with ConnectionPool() as cursor:
            cursor.execute("SELECT eventName FROM event_info WHERE hostID = 4")
            name = cursor.fetchone()[0]
        return name

    def test_main_page(self):
        test_event = Event("test event", "this is a test", self.hostID, "high school" ,"11.12.2020", "15.15", "2 hours", "EEB", "ITU AYAZAGA",
                           100)
        name = self.insert_check(test_event)
        self.assertEqual(name, "test event")



if __name__ == "__main__":
    unittest.main()
