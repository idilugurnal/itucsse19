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
        self.is_validated = None

    def __repr__(self):
        return "<User {}>".format(self.username)

    def save_to_db(self):
        with ConnectionPool() as cursor:
            print('conn')
            cursor.execute('INSERT INTO user_info(firstname, lastname, username, email, passwrd, institution, userType ) '
                           'VALUES(%s,%s,%s,%s,%s,%s,%s);'
                           ,(self.first_name, self.last_name, self.username, self.email, self.password,self.institution, self.userType ))
    @classmethod
    def get_with_email(cls,mail):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT * FROM user_table WHERE email = %s', (mail,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(id = user_data[0], username = user_data[1], first_name = user_data[2], surname = user_data[3], email = user_data[4] , password= user_data[5])
            else:
                return

    def check_password(self,passwrd):
        if self.password == passwrd:
            return 1
        else:
            return 0

