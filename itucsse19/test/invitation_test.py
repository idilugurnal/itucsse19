import os
import unittest
from dbconn import Database
from invitation import Invitation
from dbconn import ConnectionPool
from flask_bcrypt import Bcrypt
from flask import Flask

Database.initialise()
app = Flask(__name__)

class InvitationTest(unittest.TestCase):

    def setUp(self):
        self.invitationID = None
        bcrypt = Bcrypt(app)
        hashed_pass = bcrypt.generate_password_hash("1234567890").decode('utf-8')
        with ConnectionPool() as cursor:
            cursor.execute("INSERT INTO user_info(firstname, lastname, username, email, passwrd, institution, usertype)"
                           "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                           ("test_name", "test_sur", "testusername", "test@test.com", hashed_pass, "test_institution",
                            "University Representative"))

            cursor.execute("SELECT userid FROM user_info where username = 'testusername'")
            self.invitor_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO user_info(firstname, lastname, username, email, passwrd, institution, usertype)"
                           "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                           ("test_name2", "test_sur2", "testusername2", "test@test2.com", hashed_pass, "test_institution22",
                            "High School Student"))

            cursor.execute("SELECT userid FROM user_info where username = 'testusername2'")
            self.invitee_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO institution_info(institutionName, webAdress, info, contactInfo, representativeId, isRegistered) "
                "VALUES(%s,%s,%s,%s,%s,%s)",
                ("NEW INSTITUTION", "new.new.com", "new information", "0000", self.invitor_id, True))

            cursor.execute("SELECT institutionID FROM institution_info where webAdress = 'new.new.com'")
            self.hostID = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO event_info(eventName, info, hostId, hostType, eventDate, eventTime, duration, venue, address, quota) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                ("test event", "test info", self.hostID, "university", "10.10.2020", "15.15","2 hours", "EEB", "test addres", 200))

            cursor.execute("SELECT eventID FROM event_info where eventName = 'test event'")
            self.eventID = cursor.fetchone()[0]




    def tearDown(self):
        with ConnectionPool() as cursor:
            cursor.execute("Delete from user_info where username = 'testusername'")
            cursor.execute("Delete from user_info where username = 'testusername2'")
            cursor.execute("Delete from institution_info where webAdress = 'new.new.com'")
            cursor.execute("Delete from event_info where hostID = %s" , (self.hostID,))
            cursor.execute("Delete from invitation_info where invitationID = %s", (self.invitationID,))

    def insert_check(self, invitation):
        self.invitationID = invitation.save_to_db()
        with ConnectionPool() as cursor:
            cursor.execute("SELECT message FROM invitation_info WHERE invitationID = %s" , (self.invitationID,))
            message = cursor.fetchone()[0]
        return message

    def test_insert(self):
        invitation = Invitation(self.eventID,self.invitee_id, self.invitee_id, False, False, "test message", "15.15")
        self.invitationID = invitation.save_to_db()
        with ConnectionPool() as cursor:
            cursor.execute("SELECT message FROM invitation_info WHERE invitationID = %s", (self.invitationID,))
            message = cursor.fetchone()[0]
        self.assertEqual(message, "test message")



if __name__ == "__main__":
    unittest.main()
