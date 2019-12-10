from dbconn import ConnectionPool


class Invitation():

    def __init__(self, eventID, inviteeID, invitorID, isSeen, isAccepted, message, invitationTime):

        self.eventID = eventID
        self.inviteeID = inviteeID
        self.invitorID = invitorID
        self.isSeen = isSeen
        self.isAccepted = isAccepted
        self.message = message
        self.invitationTime = invitationTime

    def save_to_db(self):
        with ConnectionPool() as cursor:
            cursor.execute(
                "INSERT INTO invitation_info(eventID, inviteeID, invitorID, isSeen, isAccepted, message, invitationTime) VALUES(%s,%s,%s,%s,%s,%s,%s);"
                , (self.eventID, self.inviteeID, self.invitorID, self.isSeen, self.isAccepted, self.message, self.invitationTime))