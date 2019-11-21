import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
                   "DROP TABLE IF EXISTS volunteers CASCADE;",
                   "DROP TABLE IF EXISTS addresses CASCADE;",
                   "DROP TABLE IF EXISTS notifications CASCADE;",
		           "DROP TABLE IF EXISTS invitation_info CASCADE;",
                   "DROP TABLE IF EXISTS participants CASCADE;",
                   "DROP TABLE IF EXISTS event_info CASCADE;",
                   "DROP TABLE IF EXISTS institution_info CASCADE;",
                   "DROP TABLE IF EXISTS user_info CASCADE;",
                   "CREATE TABLE user_info ("
                                           "userID serial not null unique,"
                                           "userType user_type not null,"
                                           "firstname varchar(50) not null,"
                                           "lastname varchar(50) not null,"
                                           "email varchar(100) not null unique,"
                                           "institution varchar(255) not null,"
                                           "passwrd varchar(255) not null check (length(passwrd)>9),"
                                           "isValidated boolean not null default false,"
                                           "PRIMARY KEY(userID)"
                                           ");",
                   "CREATE TABLE institution_info ( "
                                        	"institutionID serial not null unique, "
                                        	"institutionName varchar(255) not null unique, "
                                        	"webAdress varchar(255) not null unique, "
                                        	"iinfo varchar(255), "
                                        	"contactInfo varchar(255) not null,"
                                        	"representativeID int,"
                                        	"isRegistered bool default false, "
                                        	"primary key(institutionID), "
                                        	"foreign key(representativeID) references user_info(userID) on delete set null on update cascade "
                   ");",
		           "CREATE TABLE event_info ("
	                                       "eventID serial not null unique,"
	                                       "eventName varchar(255) not null unique,"
	                                       "info varchar(255) not null,"
	                                       "hostType host_type not null,"
	                                       "hostID int not null,"
	                                       "eventDate varchar(255) not null,"
	                                       "eventTime varchar(255) not null,"
	                                       "duration varchar(20) not null,"
					                       "primary key(eventID),"
    	                                   "foreign key(hostID) references institution_info(institutionID) on delete cascade on update cascade"
                                            ");",
                   "CREATE TABLE participants ( "
                                        	"participantID int not null, "
                                        	"eventID int not null, "
                                            "primary key(participantID, eventID),"
                                        	"foreign key(participantID) references user_info(userID) on delete cascade on update cascade,"
                                        	"foreign key(eventID) references event_info(eventID) on delete cascade on update cascade"
                   "); ",
                   "CREATE TABLE invitation_info ( "
                                        	"invitationID serial not null unique,"
                                        	"eventID int not null,"
                                            "inviteeID int not null,"
                                        	"invitorID int not null,"
                                        	"isSeen bool not null default false, "
                                        	"isAccepted bool not null default false,"
                                        	"message varchar(500) not null,"
                                        	"invitationTime varchar(255) not null,"
                                            "primary key(invitationID),"
                                        	"foreign key(eventID) references event_info(eventID) on delete cascade on update cascade,"
                                        	"foreign key(inviteeID) references user_info(userID) on delete cascade on update cascade,"
                                        	"foreign key(invitorID) references user_info(userID) on delete cascade on update cascade"
                ");",
                "CREATE TABLE notifications("
                                        	"notificationID serial not null unique, "
                                        	"actionType notif_type not null,"
                                        	"receiver int not null,"
                                        	"sender int, "
                                        	"link varchar(255),"
                                        	"notifTime varchar(255) not null,"
                                        	"foreign key(sender) references user_info(userID) on delete set null on update cascade,"
                                        	"foreign key(receiver) references user_info(userID) on delete cascade on update cascade"
                ");",
                "CREATE TABLE addresses( "
                                        	"addressID serial not null unique,"
                                        	"institutionID int not null,"
                                        	"city varchar(500) not null, "
                                        	"address varchar(500) not null unique, "
                                        	"primary key(addressID), "
                                        	"foreign key(institutionID) references institution_info(institutionID) on delete cascade on update cascade "
                ");",
                "CREATE TABLE volunteers( "
                                        	"volunteerID serial not null unique, "
                                        	"eventID int not null unique, "
                                        	"isAssigned bool not null default false,"
                                        	"primary key(volunteerID, eventID),"
                                        	"foreign key(volunteerID) references user_info(userID) on delete cascade on update cascade,"
                                        	"foreign key(eventID) references event_info(eventID) on delete cascade on update cascade"                       
                ");",

                 ]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
