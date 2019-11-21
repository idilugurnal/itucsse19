create table institution_info(
	institutionID serial not null unique,
	institutionName varchar(255) not null unique,
	webAdress varchar(255) not null unique,
	info varchar(255),
	contactInfo varchar(255) not null,
	representativeID int not null,
	primary key(institutionID),
	foreign key(representativeID)
		references user_info(userID)
		on delete cascade
		on update cascade
)