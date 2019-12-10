create type host_type as enum ('university', 'high school');

create table event_info(
	eventID serial not null unique,
	eventName varchar(255) not null unique,
	info varchar(255) not null,
	hostID int not null,
	hostType host_type not null,
	eventDate varchar(255) not null,
	eventTime varchar(255) not null,
	duration varchar(20) not null,
	venue varchar(255) not null,
	address varchar(255) not null,
	quota int,
	primary key(eventID),
	foreign key(hostID)
		references institution_info(institutionID)
		on delete cascade
		on update cascade
)