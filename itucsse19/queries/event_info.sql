create type host_type as enum ('university', 'high school');

create table event_info(
	eventID serial not null unique,
	eventName varchar(255) not null unique,
	info varchar(255) not null,
	hostType host_type not null,
	hostID int not null,
	eventDate varchar(255) not null,
	eventTime varchar(255) not null,
	duration varchar(20) not null,
	primary key(eventID),
	foreign key(hostID)
		references institution_info(institutionID)
		on delete cascade
		on update cascade
)