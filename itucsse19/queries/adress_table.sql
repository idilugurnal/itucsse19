create table adresses(
	adressID serial not null unique,
	institutionID int not null,
	city varchar(500) not null,
	adress varchar(500) not null unique,
	primary key(adressID),
	foreign key(institutionID)
		references institution_info(institutionID)
		on delete cascade
		on update cascade
)