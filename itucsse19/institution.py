from dbconn import ConnectionPool

class Address:
    def __init__(self, id, city, address ):
        self.ID = id
        self.city = city
        self.address = address


class Institution:

    def __init__(self, institutionID, institutionName, webAdress, info, contactInfo, ):
        self.institutionID = institutionID
        self.institutionName = institutionName
        self.webAdress = webAdress
        self.info = info
        self.contactInfo = contactInfo
        self.adresses = []


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
                return cls(institutionID=ins_info[0], institutionName=ins_info[1], webAdress=ins_info[2], info=ins_info[3],
                           contactInfo=ins_info[4] )
            else:
                return

    @classmethod
    def get_by_name(cls, institutionName):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT * FROM institution_info WHERE institutionName = %s', (institutionName,))
            ins_info = cursor.fetchone()
            if ins_info:
                return cls(institutionID=ins_info[0], institutionName=ins_info[1], webAdress=ins_info[2], info=ins_info[3],
                           contactInfo=ins_info[4])
            else:
                return

    def get_addresses(self):
        with ConnectionPool() as cursor:
            cursor.execute('SELECT * FROM addresses WHERE institutionID = %s', (self.institutionID,))
            addresses = cursor.fetchall()
        for address in addresses:
            add = Address(address[0], address[2], address[3], )
            self.adresses.append(add)

