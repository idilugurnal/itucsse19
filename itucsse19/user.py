import psycopg2
from dbconn import ConnectionPool
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, first_name , last_name, username , email, password , institution , userType):
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
            cursor.execute("INSERT INTO user_info(firstname, lastname, username, email, passwrd, institution, usertype ) VALUES(%s,%s,%s,%s,%s,%s,%s);"
                           ,(self.first_name, self.last_name, self.username, self.email, self.password,self.institution, self.userType ))

