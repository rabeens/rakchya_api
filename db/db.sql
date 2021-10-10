-- drop database if exists rakchya;
create database if not exists rakchya;

use rakchya;

SET FOREIGN_KEY_CHECKS = 0;



drop table if exists users;
create table users(
	id int auto_increment primary key,
	fname varchar(255),
	lname varchar(255),
	email varchar(255),
	contact_number varchar(15),
	token varchar(255),
	password varchar(255),
	active bool default 0,
	status bool default 0,
	last_login timestamp,
	reset_password_id varchar(255),
	address1 varchar(255),
	address2 varchar(255),
	city varchar(255),
	state varchar(255),
	country varchar(255),
	dob timestamp,
	created_at timestamp default now(), 
	created_by int
);

drop table if exists symptoms;
create table symptoms (
	id int auto_increment primary key, 
	name varchar(255),
	type varchar(10) default 'Symptoms' comment 'can be ["symptoms" or "category"]',
	description varchar(255),
	icon varchar(255),
	active bool default 0,
	created_at timestamp default now(), 
	created_by int
);

drop table if exists doctors;
create table doctors (
	id int auto_increment primary key, 
	user_id int,
	description varchar(255),
	rating int default 0,
	symptom_id int, 
	created_at timestamp default now(), 
	created_by int,
	icon varchar(255),
	foreign key (user_id) references users(id) on delete cascade,
	foreign key (symptom_id) references symptoms(id) on delete cascade
);

drop table if exists doc_to_symptoms_mapping;
create table doc_to_symptoms_mapping (
	id int auto_increment primary key, 
	doc_id int,
	symptom_id int,
	foreign key (doc_id) references doctors(id) on delete cascade,
	foreign key (symptom_id) references symptoms(id) on delete cascade
);



drop table if exists cases;
create table cases (
	id int auto_increment primary key, 
	doc_id int,
	client_id int, 
	symptom_id int,
	create_date timestamp default now(), 
	is_history_taken bool default 0, 
	severity int default 0, 
	is_paid bool default 0,
	is_active bool default 1,

	created_at timestamp default now(), 
	created_by int,	
	
	foreign key (doc_id) references doctors(id)  on delete cascade,
	foreign key (client_id) references users(id)  on delete cascade,
	foreign key (symptom_id) references symptoms(id)  on delete cascade
);


drop table if exists banners;
create table banners (
	id int auto_increment primary key,
	banner_json json,
	client_id int,
	is_promo bool default 0,
	is_advertisement bool default 1,
	created_at timestamp default now(), 
	created_by int,	
	foreign key (client_id) references users(id)  on delete cascade
) comment="for banner_json, required_fields are {type, msg, link[{linkpath}, if link is rquired, else ignore], linkType{'route', if need to route within app, else ignore}}, type can be [text, image, route]";


drop table if exists product_categories;
create table product_categories (
	id int auto_increment primary key,
	name varchar(255),
	description varchar(255),
	is_active bool default 0,
	icon varchar(255),
	created_at timestamp default now(), 
	created_by int
);


drop table if exists products;
create table products (
	id int auto_increment primary key,
	name varchar(255),
	description varchar(255),
	category_id int,
	price float(10,2) default 0.0,
	stock_qty float(10,0) default 0.0,
	is_active bool default 0,
	created_at timestamp default now(), 
	created_by int,	
	foreign key (category_id) references product_categories(id)
);

drop table if exists carts;
create table carts (
	id int auto_increment primary key,
	client_id int,
	product_id int,
	cart_add_date timestamp default now(),
	amt float(10,2) default 0.0,
	quantity float(10,2) default 0.0,
	foreign key (client_id) references users(id) on delete cascade,
	foreign key (product_id) references products(id) on delete cascade
);



drop table if exists chat_msg;
create table chat_msg (
	id int auto_increment primary key,
	case_id int,
	sender int,
	msg varchar(255),
	ts timestamp default now(),
	foreign key (sender) references users(id) on delete cascade,
	foreign key (case_id) references cases(id) on delete cascade
);



drop table if exists okhati_requests;
create table okhati_requests (
	request_id int auto_increment primary key,
	client_id int,
	invoice_asset_path varchar(255),
	progress varchar(255),
	requested_date timestamp default now(),
	is_confirmed bool default 0,
	is_paid bool default 0,
	is_active bool default 0,
	is_closed bool default 0,

	amt float(10,2) default 0.0,
	service_charge float(10,2) default 0.0,
	delivery_charge float(10,2) default 0.0,
	quantity float(10,2) default 0.0,
	tax float(10,2) default 0.0,
	currency_symbol varchar(10) default 'NPR',
	assignee int,
	foreign key (client_id) references users(id) on delete cascade
);




SET FOREIGN_KEY_CHECKS = 1;