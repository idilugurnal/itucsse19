create table university_info(
	universityID serial not null unique,
	universityName varchar(255) not null unique,
	webAdress varchar(255) not null unique,
	info varchar(255),
	city varchar(255) not null,
	contactInfo varchar(255) not null,
	representativeID int not null,
	primary key(universityID),
	foreign key(representativeID)
		references user_info(userID)
		on delete cascade
		on update cascade
)