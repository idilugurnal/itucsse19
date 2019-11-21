create table participants(
	participantID int not null,
	eventID int not null,
	primary key(participantID, eventID),
	foreign key(participantID)
		references user_info(userID)
		on delete cascade
		on update cascade,
	foreign key(eventID)
		references event_info(eventID)
		on delete cascade
		on update cascade
)