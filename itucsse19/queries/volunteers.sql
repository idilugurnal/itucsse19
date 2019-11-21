create table volunteers(
	volunteerID serial not null unique,
	eventID int not null unique,
	isAssigned bool not null default false,
	primary key(volunteerID, eventID),
	foreign key(volunteerID)
		references user_info(userID)
		on delete cascade
		on update cascade,
	foreign key(eventID)
		references event_info(eventID)
		on delete cascade
		on update cascade
)