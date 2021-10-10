insert into users 
	(
		id, fname, lname, email, contact_number, token, password, active
	)
	values(
		1,
		'Rabindra',
		'Neupane',
		'neupanerabeen@gmail.com',
		'9841497332',		
		'1f267ef999e13da9f18f996639e65829',
		'1f267ef999e13da9f18f996639e65829',
		1
	),
	(
		2,
		'Rabeens',
		'Sharma',
		'info@rabeens.com',
		'9841497333',		
		'1f267ef999e13da9f18f996639e65830',
		'1f267ef999e13da9f18f996639e65829',
		1
	);

insert into symptoms (id, name, type, description) values
	(1, "Fever", "symptoms", "Mild fever is usual"),
	(2, "ENT", "category", "ear nose throat");

insert into doctors (id, user_id, description, symptom_id ) values
	(1, 2, "Dr rabeens for fever", 1);

insert into doc_to_symptoms_mapping (doc_id, symptom_id ) values
	(1, 1);

insert into product_categories (name, is_active, description) values
	("Cat 1", 1, "Category 1 description"),
	("Cat 2", 1, "Category 2 description");


insert into banners (id, banner_json, client_id, is_promo, is_advertisement) values 
	(1, '{"type":"text","link":"http://rakchya.com","linkType":"external", "msg":"Promoting Rakchya", "style":{"fontSize":24, "textAlign":"center", "color":"blue" }}', 1, 1,0),
	(2, '{"type":"text","link":"http://rabeens.com","linkType":"external", "msg":"Visit developer: Rabeens.com", "style":{"fontSize":24, "textAlign":"center", "color":"blue" }}', 1, 0,1);