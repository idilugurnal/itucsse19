from dbconn import ConnectionPool


class Institution():

    def __init__(self, institutionName, webAdress, info, contactInfo, ):
        self.institutionName = institutionName
        self.webAdress = webAdress
        self.info = info
        self.contactInfo = contactInfo


    def update_information(self):
        with ConnectionPool() as cursor:
            cursor.execute('UPDATE institution_info set webAdress = %s, info = %s, contactInfo = %s WHERE institutionName = %s',
                           (self.webAdress, self.info, self.contactInfo, self.institutionName))

    def register(self, representativeID):
        with ConnectionPool() as cursor:
            cursor.execute('UPDATE institution_info set representativeID = %s, isRegistered = %s WHERE institutionName = %s',
                           (representativeID, True, self.institutionName))

    @classmethod
    def get_by_representative(cls, representativeID):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT * FROM institution_info WHERE representativeID = %s', (representativeID,))
            ins_info = cursor.fetchone()
            if ins_info:
                return cls(institutionName=ins_info[1], webAdress=ins_info[2], info=ins_info[3], contactInfo=ins_info[4] )
            else:
                return
