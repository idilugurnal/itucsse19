create type user_type as enum ('University Student', 'High School Student', 'Universiy Represantative', 'High School Representative');
create table user_info(
	userID serial not null unique,
	userType user_type not null,
	username varchar(255) not null unique,
	firstname varchar(50) not null,
	lastname varchar(50) not null,
	email varchar(100) not null unique,
	institution varchar(255) not null,
	passwrd varchar(255) not null check (length(passwrd)>9),
	isValidated boolean not null default false,
	primary key(userID)
)