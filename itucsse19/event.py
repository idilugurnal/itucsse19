from flask import Flask, jsonify,render_template, url_for, flash , redirect, request, abort,request, current_app, send_from_directory
from flask_login import LoginManager
from flask_login.utils import login_required, login_user, current_user, logout_user
from dbconn import Database
from flask_bcrypt import Bcrypt
import forms
from user import User
from dbconn import ConnectionPool


class Event():
    def __init__(self, event_name , info, hostID, hostType, date, time, duration, venue, address, quota, creator):

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
        self.creator = creator
        self.id = None


    def save_to_db(self):
        with ConnectionPool() as cursor:
            cursor.execute("INSERT INTO event_info(eventName, info, hostID, hostType, eventDate, eventTime, duration, venue, address, quota ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
                           ,(self.event_name, self.info, self.hostID, self.hostType, self.date, self.time,self.duration, self.venue, self.address, self.quota ))

            cursor.execute("SELECT eventID FROM event_info WHERE eventName = %s AND info = %s AND venue = %s AND eventTime = %s",
                           (self.event_name, self.info, self.venue, self.time))
            self.id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO participants(participantID , eventID) VALUES(%s,%s)" , (self.creator , self.id))

        return self.id

