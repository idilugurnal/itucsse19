create table addresses(
	addressID serial not null unique,
	institutionID int not null,
	city varchar(500) not null,
	address varchar(500) not null unique,
	primary key(addressID),
	foreign key(institutionID)
		references institution_info(institutionID)
		on delete cascade
		on update cascade
)