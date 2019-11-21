create table adresses(
	adressID serial not null unique,
	schoolID int not null,
	adress varchar(500) not null unique,
	primary key(adressID),
	foreign key(schoolID)
		references school_info(schoolID)
		on delete cascade
		on update cascade
)