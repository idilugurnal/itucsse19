from dbconn import ConnectionPool


class Event():
    def __init__(self, event_name , info, hostID, hostType, date, time, duration, venue, address, quota, isOpen, id=None):

        self.event_name = event_name
        self.info = info
        #HostID is the id of the institution
        self.hostID = hostID
        self.hostType = hostType
        self.date = date
        self.time = time
        self.duration = duration
        self.venue = venue
        self.address = address
        self.quota = quota
        self.isOpen = isOpen
        self.id = id

    def get_id(self):
        with ConnectionPool() as cursor:
            cursor.execute(
                "SELECT eventID FROM event_info WHERE eventName = %s AND info = %s AND venue = %s AND eventTime = %s",
                (self.event_name, self.info, self.venue, self.time))
            self.id = cursor.fetchone()[0]

    def save_to_db(self, creator = None):
        with ConnectionPool() as cursor:
            cursor.execute("INSERT INTO event_info(eventName, info, hostID, hostType, eventDate, eventTime, duration, venue, address, quota ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                           ,(self.event_name, self.info, self.hostID, self.hostType, self.date, self.time,self.duration, self.venue, self.address, self.quota ))

            cursor.execute("SELECT eventID FROM event_info WHERE eventName = %s AND info = %s AND venue = %s AND eventTime = %s",
                           (self.event_name, self.info, self.venue, self.time))
            self.id = cursor.fetchone()[0]

            if creator:
                cursor.execute("INSERT INTO participants(participantID , eventID) VALUES(%s,%s)" , (creator , self.id))

        return self.id

    @classmethod
    def get_with_id(cls, my_id):
        with ConnectionPool() as cursor:
            cursor.execute("SELECT eventName, info, hostID, hostType, eventDate, eventTime, duration, venue, address, quota, isOpen"
                           " FROM event_info WHERE eventID = %s", (my_id,))
            event = cursor.fetchone()
            return cls(event_name=event[0], info=event[1], hostID=event[2], hostType=event[3], date=event[4], time=event[5],
                       duration=event[6],venue= event[7], address=event[8], quota=event[9], isOpen=event[10], id=my_id)
