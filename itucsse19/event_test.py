import os
import unittest
from dbconn import Database
from event import Event
from dbconn import ConnectionPool

Database.initialise()

class EventTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def insert_check(self, event):
        test_event_id = event.save_to_db()
        with ConnectionPool() as cursor:
            cursor.execute("SELECT eventName FROM event_info WHERE hostID = 4")
            name = cursor.fetchone()[0]
        return name

    def test_main_page(self):
        test_event = Event("test event", "this is a test", 4, "high school" ,"11.12.2020", "15.15", "2 hours", "EEB", "ITU AYAZAGA",
                           100)
        name = self.insert_check(test_event)
        self.assertEqual(name, "test event")



if __name__ == "__main__":
    unittest.main()
