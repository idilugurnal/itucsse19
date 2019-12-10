create table invitation_info(
	invitationID serial not null unique,
	eventID int not null,
	inviteeID int not null,
	invitorID int not null,
	isSeen bool not null default false,
	isAccepted bool not null default false,
	message varchar(500) not null,
	invitationTime varchar(255) not null,
	primary key(invitationID),
	foreign key(eventID)
		references event_info(eventID)
		on delete cascade
		on update cascade,
	foreign key(inviteeID)
		references user_info(userID)
		on delete cascade
		on update cascade,
	foreign key(invitorID)
		references user_info(userID)
		on delete cascade
		on update cascade
)

alter table event_info add constraint name_info_venue UNIQUE(inviteeID,invitorID, eventTime)