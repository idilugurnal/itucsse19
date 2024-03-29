import psycopg2
from dbconn import ConnectionPool
from flask_login import UserMixin
from event import Event


class User(UserMixin):

    def __init__(self, first_name , last_name, username , email, password , institution , userType, id=None):
        self.id = id
        self.username = username
        self.userType = userType
        self.institution = institution
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.username)

    def save_to_db(self):
        with ConnectionPool() as cursor:
            if self.userType == "University Representative" or self.userType == "High School Representative":
                cursor.execute("SELECT isRegistered FROM institution_info WHERE institutionName = %s" , (self.institution,))
                val = cursor.fetchone()
                if val is not None:
                    flash(f'An error occured!', 'error')
                    return
            cursor.execute("INSERT INTO user_info(firstname, lastname, username, email, passwrd, institution, usertype ) VALUES(%s,%s,%s,%s,%s,%s,%s);"
                           ,(self.first_name, self.last_name, self.username, self.email, self.password,self.institution, self.userType ))

    @classmethod
    def get_by_email(cls, mail):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT * FROM user_info WHERE email = %s', (mail,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(id=user_data[0], username=user_data[2], userType=user_data[1], institution=user_data[6], first_name=user_data[3], last_name=user_data[4],
                           email=user_data[5], password=user_data[7])
            else:
                return

    @classmethod
    def get_by_username(cls, username):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT * FROM user_info WHERE username = %s', (username,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(id=user_data[0], username=user_data[2], userType=user_data[1], institution=user_data[6], first_name=user_data[3], last_name=user_data[4],
                           email=user_data[5], password=None)
            else:
                return

    def get_id(self):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT userid FROM user_info WHERE username = %s', (self.username,))
            user = cursor.fetchone()
            if user is None:
                return
            else:
                return user[0]

    def get_events(self):
        result_list = []
        with ConnectionPool() as cursor:
            userid = self.get_id()
            cursor.execute("SELECT eventID FROM participants WHERE participantID = %s" , (userid,))
            event_list= cursor.fetchall()
            for eventID in event_list:
                event_class = Event.get_with_id(eventID[0])
                result_list.append(event_class)
        return result_list

    def get_institution_events(self):
        result_list = []
        with ConnectionPool() as cursor:
            userid = self.get_id()
            cursor.execute("SELECT institutionid FROM institution_info WHERE institutionName = %s" , (self.institution,))
            institution_id = cursor.fetchone()[0]
            cursor.execute("SELECT eventID FROM event_info WHERE hostID = %s", (institution_id,))
            event_list = cursor.fetchall()
            cursor.execute("SELECT eventID FROM participants WHERE participantID = %s", (userid,))
            my_events = cursor.fetchall()
            for eventID in event_list:
                if eventID not in my_events:
                    event_class = Event.get_with_id(eventID[0])
                    result_list.append(event_class)
        return result_list
