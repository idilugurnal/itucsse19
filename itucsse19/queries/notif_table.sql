create type notif_type as enum('Event Update', 'Event Cancelation', 'Assigned to Event', 'Participation', 'Invitation'); 

create table notifications(
	notificationID serial not null unique,
	actionType notif_type not null,
	receiver int not null,
	sender int,
	link varchar(255),
	notifTime varchar(255) not null,
	foreign key(sender)
		references user_info(userID)
		on delete set null
		on update cascade,
	foreign key(receiver)
		references user_info(userID)
		on delete cascade
		on update cascade
	
)