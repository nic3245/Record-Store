/*
*******  record_store_ddl.sql. *******
Benoit Cambournac, Nicholas Labuda, Malick Tobe
CS 3200 - Durant
Record Store Database Project

Creating the database to represent a record store
- create the schema and tables
- populating the tables
- creating procedures, functions, triggers
*/

drop database if exists record_store;
create database record_store;
use record_store;

/************* Table Definitions ****************/

-- Table for record store employees, with boolean to represent the manager (is_manager
create table employee(
	emp_id int primary key auto_increment,
    full_name varchar(100) not null,
    salary int not null,
    is_manager bool default false not null
);

-- table for all the shifts being worked at the store (same every week, changes are allowed)
create table shifts(
	shift_id int primary key auto_increment,
    week_day enum ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday') not null,
    start_hr int not null,
    end_hr int not null,
    assigned_employee int, -- some shifts can be null (description in paper)
    constraint shift_employee_fk
		foreign key (assigned_employee) references employee(emp_id)
        on update cascade on delete set null
);

-- table for customers of the record store
create table customer(
	c_id int primary key auto_increment,
    first_name varchar(30) not null,
    last_name varchar(30) not null,
    email varchar(75), -- some instore customers can opt to not provide email
    cc_num int -- also optional for customers who pay cash
);

-- table of the store sections where items are found in
create table section(
	section_id int primary key auto_increment,
    title varchar(50) not null, -- the 'title of the section'(basic theme of what items are in it)
    description varchar(200) not null
);

-- table for item parent class (used by record, equipment, record_player)
-- items aren't deleted -- if they are stopped being sold -- quantity remains at 0
create table item(
	item_id int primary key auto_increment,
	price numeric(10,2) not null,
    quantity int default 0 not null, -- quantity in stock of each item (can stay at 0)
    section_id int,
    constraint item_section_fk
		foreign key (section_id) references section(section_id)
        on update cascade on delete set null -- just sets to the defualt (online-only section - 0)
);
-- need trigger to decrease quantity?

-- table for artists of the records being sold
create table artist(
	artist_id int primary key auto_increment,
    name varchar(100) not null,
    lead_singer varchar(75) not null
);

-- table for genres of music represented in the store
create table genre(
	genre_id int primary key auto_increment,
    genre_name varchar(100) not null
);

-- table of the item subclass Record for the records in the store
create table records(
	-- record_id int primary key auto_increment,
    -- opted to make weak entities instead
    item_id int not null,
    name varchar(100) not null,
    release_year int not null,
    artist_id int not null,
    genre_id int not null,
    constraint record_item_fk
		foreign key (item_id) references item(item_id)
        on update cascade on delete cascade,
	constraint record_artist_fk
		foreign key (artist_id) references artist(artist_id)
        on update cascade on delete cascade,
	constraint record_genre_fk
		foreign key (genre_id) references genre(genre_id)
        on update cascade on delete cascade 
	-- don't want to delete the artist or genre if the artist or genre are removed from the DB
);

-- table for subclass Equipment - music related gadgets and equipment sold at the store
create table equipment(
	-- e_id int primary key auto_increment,
	-- opted to make weak entities instead
    item_id int not null,
    name varchar(50) not null,
    description varchar(200) not null,
    manufacturer varchar(50) not null,
    constraint equipment_item_fk
		foreign key (item_id) references item(item_id)
        on update cascade on delete cascade
);

-- table for subclass for the Record Players sold in the store
create table record_player(
	-- rp_id int primary key auto_increment,
	-- opted to make weak entities instead
    item_id int not null,
    disc_size enum ('7', '10', '12') default '10' not null,
    manufacturer varchar(50) not null,
    year int not null,
    model varchar(50) not null,
    bluetooth bool default false not null, -- whether player is bleutooth enabled?
	constraint rplayer_item_fk
		foreign key (item_id) references item(item_id)
        on update cascade on delete cascade
);

-- table for orders placed at the store or online
create table orders(
	order_id int primary key auto_increment,
    c_id int not null,
    location enum ('Online', 'In-Store') default 'In-Store' not null,
    num_items int default 0 not null,
    total numeric(10,2) default 0.00 not null,
    constraint order_customer_fk
		foreign key (c_id) references customer(c_id)
        on update cascade on delete cascade 
);

-- table for all the items in each order
create table order_items(
	order_id int,
    item_id int,
    quantity int default 1 not null,
    primary key (order_id, item_id),
    constraint orderItem_order_fk
		foreign key (order_id) references orders(order_id)
        on update cascade on delete cascade,
	constraint orderItem_item_fk
		foreign key (item_id) references item(item_id)
        on update cascade on delete cascade
);


/************* Functions and Procedures Definitions ****************/
delimiter //

-- add artist to the artist table
create procedure add_artist(
	in artist_name varchar(100),
    in singer varchar(75)
)
begin
	insert into artist(artist_id, name, lead_singer)
		values (default, artist_name, singer);
end//

-- add a genre to the database
create procedure add_genre(
	in g_name varchar(100)
)
begin
	insert into genre(genre_id, genre_name)
    values (default, g_name);
end//

-- add a customer to the database
create procedure add_customer(
	in first_n varchar(30),
    in last_n varchar(50),
    in email_p varchar(75),
    in credit_card int
    -- email and CC can both be null and function should still work
)
begin
	-- create the customer
	insert into customer(c_id, first_name, last_name, email, cc_num)
    values (default, first_n, last_n, email_p, credit_card);
    
    -- return the customer id
    select max(c_id)
    from customer;
end//

-- add an employee to the database
create procedure add_employee(
	in emp_name varchar(100),
    in salary_p int
)
begin
	insert into employee(emp_id, full_name, salary, is_manager)
    values (default, emp_name, salary_p, false);
end//

-- add a manager to the database (seperate from add_emp to easily differentiate managers)
create procedure add_manager(
	in manager_name varchar(100),
    in salary_p int
)
begin
	insert into employee(emp_id, full_name, salary, is_manager)
    values (default, manager_name, salary_p, true);
end//

-- function to create a new item in the database and return the created items id
create function add_item(
	item_price numeric(10, 2),
    item_quantity int,
    store_sectionid int
)
returns int
deterministic contains sql
begin
	declare i_id int;
    
	insert into item(item_id, price, quantity, section_id)
    values (default, item_price, item_quantity, store_sectionid);
    
    -- get the id of the recently inserted item id
    select item_id into i_id
    from item
	order by item_id desc
    limit 1; 
    
    -- returning the created item's id
    return i_id;
end//

-- procedure to insert a piece of equipment to the database
create procedure add_equipment(
	in e_name varchar(50),
    in e_description varchar(200),
    in e_manufacturer varchar(50),
    in e_price numeric(10,2),
    in e_quantity int,
    in section int
)
begin
	-- create the parent item and get the id
	declare e_item int;
    set e_item = add_item(e_price, e_quantity, section);
    
    -- now create the equipment
    insert into equipment(item_id, name, description, manufacturer)
    values (e_item, e_name, e_description, e_manufacturer);
    
end//

create procedure add_record_player(
	in rp_disc_size enum ('7', '10', '12'),
    in rp_manufacturer varchar(50),
    in rp_year int,
	in rp_model varchar(50),
    in rp_bluetooth bool,
    in rp_price numeric(10,2),
    in rp_quantity int,
    in section int
)
begin
	-- create the parent item and get the id
	declare rp_item int;
    set rp_item = add_item(rp_price, rp_quantity, section);
    
    -- create the record player
    insert into record_player(item_id, disc_size, manufacturer, year, model, bluetooth)
    values (rp_item, rp_disc_size, rp_manufacturer, rp_year, rp_model, rp_bluetooth);
end//

-- procedure to add a new record to the database
create procedure add_record(
	in r_name varchar(100),
    in r_year int,
    in r_artist_id int,
    in r_genre_id int,
    in r_price numeric(10,2),
    in r_quantity int,
    in section int
)
begin
	-- create the parent item and get the id
	declare r_item int;
    set r_item = add_item(r_price, r_quantity, section);
    
    -- create the new record
    insert into records(item_id, name, release_year, artist_id, genre_id)
    values (r_item, r_name, r_year, r_artist_id, r_genre_id);
end//

-- function to create a new order in the database and return the order number
create procedure create_order(
	customer_id int,
    o_location enum ('Online' , 'In-Store')
)
begin
	declare o_id int;
    
    -- create the order for the customer
	insert into orders(order_id, c_id, location, num_items, total)
    values (default, customer_id, o_location, default, default);
    
    -- get and return the order id of the new order
    select max(order_id) into o_id
    from orders;
end//

-- procedure to add the given quantity of an item to an order
create procedure add_order_item(
	in o_id int,
    in i_id int,
    in quant int
)
begin
	declare item_price numeric(10,2);
	-- add the item and quantity to the order
	insert into order_items(order_id, item_id, quantity)
    values (o_id, i_id, quant);
    
    -- get the price of the item
    select price into item_price
    from item
    where item_id = i_id;
    
    -- calculate the price to add to the total
    set item_price = item_price * quant;
    
    -- update the order total and number of items
    update orders
    set total = total + item_price, num_items = num_items + quant
    where order_id = o_id;
    
    -- update the stock of the sold item
    update item
    set quantity = quantity - quant
    where item_id = i_id;
end//	

-- procedure to add a new shift to the schedule
create procedure add_shift(
	in week_day_p enum ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'),
    in start_h int,
    in end_h int,
    in emp_id int
)
begin
	insert into shifts(shift_id, week_day, start_hr, end_hr, assigned_employee)
    values (default, week_day_p, start_h, end_h, emp_id);
end//

-- procedure to change the employee on a certain shift
create procedure change_shift_emp(
	in s_id int,
    in emp_id int
)
begin
	update shifts
    set assigned_employee = emp_id
    where shift_id = s_id;
end//

-- procedure to check the stock of a certain item
create function check_stock(
	i_id int
)
returns int
deterministic reads sql data
begin
	declare quant int;
    
    select quantity into quant
    where item_id = i_id;
    
    return quant;
end//

-- procedure to check if an employee is manager or not
create procedure check_manager(
	in id int
)
begin
	select is_manager
    from employee
    where emp_id = id;
end//

-- procedures to view all of the records, record players, and all equipment
create procedure view_all_records()
begin
	select i.*, r.name as 'name', release_year, a.name as 'artist', g.genre_name as 'genre'
    from records r join item i using(item_id) join artist a using(artist_id)
		join genre g using(genre_id);
end//

create procedure view_all_recordplayers()
begin
	select *
    from record_player r join item i using(item_id);
end//

create procedure view_all_equipment()
begin
	select *
    from equipment e join item i using(item_id);
end//

-- procedure to view all of the records, filtered by genre
create procedure records_by_genre(
	in g_id int
)
begin
	select i.*, r.name as 'name', release_year, a.name as 'artist', g.genre_name as 'genre'
    from records r join item i using(item_id) join artist a using(artist_id)
		join genre g using(genre_id)
	where genre_id = g_id;
end//

-- procedure to view all the records sold by the given artist
create procedure records_by_artist(
	in a_id int
)
begin
	select i.*, r.name as 'name', release_year, a.name as 'artist', g.genre_name as 'genre'
    from records r join item i using(item_id) join artist a using(artist_id)
		join genre g using(genre_id)
	where r.artist_id = a_id;
end//

-- procedure to view the schedule (all the shifts)
create procedure view_schedule()
begin
	select s.*, e.full_name
    from shifts s left outer join employee e
		on s.assigned_employee = e.emp_id;
end//

-- procedure to update employee
create procedure update_employee(
	in id int,
	in e_name varchar(100),
    in sal int,
    in manager bool
)
begin
	update employee
    set full_name = e_name, salary = sal, is_manager = manager
    where e_id = id;
end//

-- procedure to update artist
create procedure update_artist(
	in id int,
    in a_name varchar(100),
    in singer varchar(75)
)
begin
	update artist
    set name = a_name, lead_singer = singer
    where artist_id = id;
end//

-- procedure to update customer
create procedure update_customer(
	in id int,
    in f_name varchar(30),
    in l_name varchar(30),
    in mail varchar(75),
    in cc int
)
begin
	update customer
    set first_name = f_name, last_name = l_name, email = mail, cc_num = cc
    where c_id = id;
end//

-- procedure to update a section
create procedure update_section(
	in id int,
    in s_title varchar(50),
    in s_description varchar(200)
)
begin
	update section
    set title = s_title and description = s_description
    where section_id = id;
end//

-- procedure to update a record
create procedure update_record(
	in id int,
    in r_price numeric(10,2),
    in r_quantity int,
    in r_name varchar(100),
    in year int,
    in genre int
)
begin
	update records
    set name = r_name, release_year = year, genre_id = genre
    where item_id = id;
    
    update item
    set price = r_price, quantity = r_quantity
    where item_id = id;
end//

-- procedure to update a record player
create procedure update_record_player(
	in id int,
    in disc enum ('7', '10', '12'),
    in manu varchar(50),
    in yr int,
    in m varchar(50),
    in blue bool,
    in r_price numeric(10,2),
    in r_quantity int
)
begin
	update record_player
    set disc_size = disc, manufacturer = manu, year = yr, model = m, bluetooth = blue
    where item_id = id;
    
    update item
    set price = r_price, quantity = r_quantity
    where item_id = id;
end//

-- procedure to update a record player
create procedure update_equipment(
	in id int,
    in r_name varchar(50),
    in descrip varchar(200),
    in manu varchar(50),
    in r_price numeric(10,2),
    in r_quantity int
)
begin
	update equipment
    set name = r_name, manufacturer = manu, description = descrip
    where item_id = id;
    
    update item
    set price = r_price, quantity = r_quantity
    where item_id = id;
end//

-- procedure to view all orders in full detail
create procedure view_all_orders()
begin
	select o.*, i.price, r.name as 'Record', e.name as 'Equipmenmt', rp.model as 'Record Player'
    from order_items o left outer join records r using (item_id)
		left outer join record_player rp using (item_id) left outer join equipment e using (item_id) 
        left outer join item i using (item_id);
end//

-- procedure to view a specific order's details
create procedure view_order_details(
	in o_id int
)
begin
	select o.*, i.price, r.name as 'Record', e.name as 'Equipmenmt', rp.model as 'Record Player'
    from order_items o left outer join records r using (item_id)
		left outer join record_player rp using (item_id) left outer join equipment e using (item_id) 
        left outer join item i using (item_id)
	where order_id = o_id;
end//

-- procedure to view all of a customer's orders
create procedure view_customer_details(
	in id int
)
begin
	select *
    from orders
    where c_id = id;
end//

-- procedure to change the section of an item
create procedure move_section(
	in i_id int,
    in s_id int
)
begin
	update item
    set section_id = s_id
    where item_id = i_id;
end//

-- procedure to delete an employee
create procedure delete_employee(
	in e_id int
)
begin
	delete from employee where emp_id = e_id;
end//

-- procedure to delete a shift
create procedure delete_shift(
	in s_id int
)
begin
	delete from shifts where shift_id = s_id;
end//

-- procedure to delete an artist
create procedure delete_artist(
	in a_id int
)
begin
	delete from artist where artist_id = a_id;
end//

-- procedure to delete a customer
create procedure delete_customer(
	in id int
)
begin
	delete from customer where c_id = id;
end//

-- procedure to delete an item
create procedure delete_item(
	in i_id int
)
begin
	delete from item where item_id = i_id;
end//

-- procedure to delete a genre
create procedure delete_genre(
	in g_id int
)
begin
	delete from genre where genre_id = g_id;
end//

-- procedure to delete a section
create procedure delete_section(
	in s_id int
)
begin
	delete from section where section_id = s_id;
end//

-- procedure to delete an order
create procedure delete_order(
	in o_id int
)
begin
	delete from orders where order_id = o_id;
end//

-- procedure to delete an order item
create procedure delete_order_item(
	in o_id int,
    in i_id int
)
begin
	delete from order_items where order_id = o_id and item_id = i_id;
end//


/**************** Populating Tables ********************/
delimiter ;
-- Employee Table
insert into employee(full_name, salary, is_manager)
values ('John David', 55000, false),
	('Mary Sue', 65000, false),
    ('Anne Marie', 45000, false),
    ('Sam Smith', 50000, false),
    ('Larry David', 62500, false),
    ('Amy Adamson', 57500, false),
    ('Sara Sullivan', 60000, false),
    ('Nick L.', 95000, true),
    ('Billy Jean', 55000, false);
    
-- shitfts tables
insert into shifts(week_day, start_hr, end_hr, assigned_employee)
values ('Monday', 7, 13, 1),
	('Monday', 12, 17, 3),
    ('Tuesday', 7, 13, 2),
    ('Tuesday', 12, 17, 6),
    ('Wednesday', 7, 13, 1),
    ('Wednesday', 12, 17, 3),
    ('Thursday', 8, 15, 2),
    ('Thursday', 14, 20, 4),
    ('Friday', 8, 15, 7),
    ('Friday', 14, 20, 5),
    ('Saturday', 7, 12, 7),
    ('Saturday', 10, 16, 8),
    ('Saturday', 13, 17, 9),
    ('Sunday', 8, 12, 6),
    ('Sunday', 10, 14, 8),
    ('Sunday', 13, 16, 9);
    
-- testing procedures
call change_shift_emp(11, 4);

-- creating the store sections
insert into section(title, description)
values ('Equipment', 'The main section for miscellaneous equipment'),
	('Record Players/Turntables', 'contains most of the record players availbe in-store'),
    ('Records and Albums', 'contains the vinyl album records of the store');

-- creating the equipment
call add_equipment('Turntable', 'high-quality record player used to play vinyl records', 'Audio-Technica', 300, 10, 1);
call add_equipment('Amplifier', 'A device that increases the power of audio signals, delivering richer sound quality', 'Yamaha', 500, 15, 1);
call add_equipment('Bookshelf Speakers', 'Compact speakers designed to fit on bookshelves or small spaces', 'Klipsch', 200, 10, 1);
call add_equipment('Headphones', 'Over-ear headphones for personal listening with excellent audio fidelity', 'Sennheiser', 150, 30, 1);
call add_equipment('Vinyl Cleaning Kit', 'A set of tools and solutions used to clean and maintain vinyl records', 'Spin-Clean', 50, 50, 1);
call add_equipment('Phono Preamp', 'A device that amplifies the low-level signals from a turntable to a line level', 'Pro-Ject', 100, 20, 1);
call add_equipment('Record Storage Cabinet', 'A stylish cabinet designed to store and organize vinyl records', 'Crosley', 250, 5, 1);
call add_equipment('Record Cleaning Machine', 'An automated device that thoroughly cleans and removes dirt from records', 'Okki Nokki', 500, 30, 1);
call add_equipment('Cartridge/Stylus', 'The needle and cartridge assembly for turntables that tracks the grooves on the record', 'Ortofon', 100, 50, 1);
call add_equipment('Vinyl Record Display Frame', 'A frame specifically designed to display vinyl records as wall art', 'Twelve Inch', 30, 25, 1);
call add_equipment('Limited Edition Box Set', 'special edition box set of records released exclusively for Record Store Day events', 'Various' , 150, 3, 1);
call add_equipment('Vinyl Record Cleaning Brush', 'A brush with anti-static properties used to remove dust and debris from records', 'Mobile Fidelity', 20, 75, 1);

-- creating the record players
call add_record_player('12', 'Audio-Technica', '2021', 'AT-LP120XUSB', true, 299.99, 20, 2);
call add_record_player('10', 'Pro-Ject', '2022', 'Debut Carbon DC', false, 399.99, 15, 2);
call add_record_player('7', 'Rega', '2020', 'Planar 1', false, 449.49, 15, 2);
call add_record_player('12', 'Technics', '2019', 'SL-1200MK7', true, 999.99, 6, 2);
call add_record_player('10', 'Denon', '2022', 'DP-400', true, 449.99, 15, 2);
call add_record_player('12', 'Pioneer', '2021', 'PLX-1000', false, 699.99, 9, 2);
call add_record_player('7', 'Sony', '2020', 'PS-HX500', true, 499.99, 13, 2);
call add_record_player('10', 'Audio-Technica', '2022', 'AT-LP5x', true, 449.99, 18, 2);
call add_record_player('12', 'Rega', '2021', 'Planar 3', false, 1099.99, 5, 2);
call add_record_player('7', 'Crosley', '2023', 'C6', true, 199.00, 22, 2);

-- adding the genres
insert into genre(genre_name)
values ('Classic Rock'),
	('Jazz'),
	('Pop'),
	('Hip Hop'),
	('Classical'),
	('Electronic'),
	('R&B'),
	('Alternative Rock');
call add_genre('Rap');
call add_genre('Heavy Metal');

-- adding the artists
insert into artist(name, lead_singer)
values('The Rolling Stones', 'Mick Jagger'),
	('Led Zeppelin', 'Robert Plant'),
	('Queen', 'Freddie Mercury'),
	('Miles Davis', 'Miles Davis'),
	('Ella Fitzgerald', 'Ella Fitzgerald'),
	('John Coltrane', 'John Coltrane'),
	('Michael Jackson', 'Michael Jackson'),
	('Madonna', 'Madonna'),
	('Taylor Swift', 'Taylor Swift'),
	('Jay-Z', 'Jay-Z'),
	('Kendrick Lamar', 'Kendrick Lamar'),
	('Cardi B', 'Cardi B'),
	('Ludwig van Beethoven', 'N/A'),
	('Wolfgang Amadeus Mozart', 'N/A'),
	('Johann Sebastian Bach', 'N/A'),
	('Daft Punk', 'N/A'),
	('The Chemical Brothers', 'N/A'),
	('Disclosure', 'N/A'),
	('Stevie Wonder', 'Stevie Wonder'),
	('Aretha Franklin', 'Aretha Franklin'),
	('Beyoncé', 'Beyoncé'),
	('Nirvana', 'Kurt Cobain'),
	('Radiohead', 'Thom Yorke'),
	('Foo Fighters', 'Dave Grohl'),
	('Eminem', 'Eminem'),
	('Kanye West', 'Kanye West'),
	('Lauryn Hill', 'Lauryn Hill'),
	('Black Sabbath', 'Ozzy Osbourne'),
	('Metallica', 'James Hetfield'),
	('Iron Maiden', 'Bruce Dickinson');
    
-- testing procedure
call add_artist('Ariana Grande', 'Ariana Grande');
call add_artist('AC/DC', 'Brian Johnson');
call add_artist('The Beatles', 'John Lennon');
call add_artist('Guns N Roses', 'Axl Rose');
call add_artist('U2', 'Bono');

-- adding records to the store
call add_record('Exile on Main St.', 1972, 1, 1, 25, 13, 3);
call add_record('Physical Graffiti', 1975, 2, 1, 30, 9, 3);
call add_record('A Night at the Opera', 1975, 3, 1, 20, 7, 3);
call add_record('Kind of Blue', 1959, 4, 2, 15, 17, 3);
call add_record('Ella Fitzgerald Sings the Cole Porter Songbook', 1956, 5, 2, 18, 12, 3);
call add_record('A Love Supreme', 1965, 6, 2, 22, 8, 3);
call add_record('Thriller', 1982, 7, 3, 25, 11, 3);
call add_record('Like a Prayer', 1989, 8, 3, 18, 19, 3);
call add_record('1989', 2014, 9, 3, 20, 10, 3);
call add_record('The Blueprint', 2001, 10, 4, 22, 15, 3);
call add_record('To Pimp a Butterfly', 2015, 11, 4, 25, 6, 3);
call add_record('Invasion of Privacy', 2018, 12, 4, 20, 14, 3);
call add_record('Symphony No. 9', 1824, 13, 5, 15, 8, 3);
call add_record('Eine kleine Nachtmusik', 1787, 14, 5, 18, 10, 3);
call add_record('Goldberg Variations', 1741, 15, 5, 22, 19, 3);
call add_record('Random Access Memories', 2013, 16, 6, 25, 7, 3);
call add_record('Surrender', 1999, 17, 6, 20, 10, 3);
call add_record('Settle', 2013, 18, 6, 18, 11, 3);
call add_record('Songs in the Key of Life', 1976, 19, 7, 25, 9, 3);
call add_record('Lady Soul', 1968, 20, 7, 22, 10, 3);
call add_record('Lemonade', 2016, 21, 7, 20, 12, 3);
call add_record('Nevermind', 1991, 22, 8, 25, 15, 3);
call add_record('OK Computer', 1997, 23, 8, 20, 7, 3);
call add_record('The Colour and the Shape', 1997, 24, 8, 18, 16, 3);
call add_record('The Marshall Mathers LP', 2000, 25, 9, 25, 19, 3);
call add_record('Late Registration', 2005, 26, 9, 20, 16, 3);
call add_record('The Miseducation of Lauryn Hill', 1998, 27, 9, 22, 13, 3);
call add_record('Paranoid', 1970, 28, 10, 25, 18, 3);
call add_record('Master of Puppets', 1986, 29, 10, 22, 13, 3);
call add_record('The Number of the Beast', 1982, 30, 10, 20, 11, 3);
call add_record('Sweetener', 2018, 31, 3, 25, 12, 3);
call add_record('Back in Black', 1980, 32, 1, 22, 14, 3);
call add_record('Abbey Road', 1969, 33, 1, 20, 16, 3);
call add_record('Appetite for Destruction', 1987, 34, 1, 18, 13, 3);
call add_record('The Joshua Tree', 1987, 35, 1, 25, 12, 3);
call add_record('Mystic Journey', 2017, 29, 6, 20, 15, 3);
call add_record('Whispers in the Wind', 2002, 26, 5, 25, 8, 3);
call add_record('Neon Dreams', 2015, 12, 6, 20, 10, 3);
call add_record('Eternal Embrace', 2006, 20, 3, 25, 11, 3);
call add_record('Soulful Journey', 2014, 15, 7, 22, 10, 3);
call add_record('Velvet Twilight', 1998, 33, 5, 18, 6, 3);
call add_record('Emerald Dreams', 2012, 19, 6, 25, 16, 3);
call add_record('Serenade in Blue', 1997, 21, 3, 25, 9, 3);
call add_record('Harmony in Motion', 2016, 14, 7, 25, 10, 3);
call add_record('Twilight Sonata', 2004, 23, 2, 18, 19, 3);
call add_record('Mystical Journey', 2011, 27, 6, 25, 17, 3);

-- adding customers to the system
call add_customer('John', 'Doe', 'johndoe@example.com', 12345678);
call add_customer('Alice', 'Smith', 'alice.smith@example.com', 6543210);
call add_customer('David', 'Johnson', 'david.johnson@example.com', 456789012);
call add_customer('Sarah', 'Williams', 'sarah.williams@example.com', 012347890);
call add_customer('Michael', 'Brown', 'michael.brown@example.com', 24567897);
call add_customer('Jessica', 'Jones', 'jessica.jones@example.com', 67890123);
call add_customer('Matthew', 'Davis', 'matthew.davis@example.com', 34567890);
call add_customer('Emily', 'Miller', 'emily.miller@example.com', 198234562);
call add_customer('Daniel', 'Wilson', 'daniel.wilson@example.com', 890125689);
call add_customer('Olivia', 'Taylor', 'olivia.taylor@example.com', 567896780);
call add_customer('Christopher', 'Anderson', 'christopher.anderson@example.com', 126789012);
call add_customer('Sophia', 'Thomas', 'sophia.thomas@example.com', 185432154);
call add_customer('James', 'Jackson', 'james.jackson@example.com', 231234567);
call add_customer('Emma', 'White', 'emma.white@example.com', 67890123);
call add_customer('Andrew', 'Harris', 'andrew.harris@example.com', 3456012);
call add_customer('Abigail', 'Martin', 'abigail.martin@example.com', 78901234);
call add_customer('Joshua', 'Thompson', 'joshua.thompson@example.com', 459876789);
call add_customer('Ava', 'Garcia', 'ava.garcia@example.com', 5678901);
call add_customer('William', 'Davis', 'william.davis@example.com', 1234678921);
call add_customer('Mia', 'Brown', 'mia.brown@example.com', 2376654);


-- creating orders for the data base and putting items in the order
insert into orders(c_id, location)
values (12, 'Online'),
	(2, 'In-Store'),
    (8, 'In-Store'),
    (4, 'In-Store'),
    (12, 'In-Store'),
    (17, 'Online'),
    (5, 'In-Store'),
    (19, 'Online'),
    (1, 'In-Store'),
    (9, 'In-Store');
    
call add_order_item(7, 53, 2);
call add_order_item(3, 19, 1);
call add_order_item(5, 41, 1);
call add_order_item(8, 12, 3);
call add_order_item(4, 30, 3);
call add_order_item(2, 61, 2);
call add_order_item(6, 39, 2);
call add_order_item(1, 68, 1);
call add_order_item(9, 24, 3);
call add_order_item(7, 56, 2);
call add_order_item(3, 8, 1);
call add_order_item(5, 32, 2);
call add_order_item(8, 47, 2);
call add_order_item(4, 16, 1);
call add_order_item(2, 64, 3);
call add_order_item(6, 36, 2);
call add_order_item(1, 62, 1);
call add_order_item(9, 21, 2);
call add_order_item(7, 49, 2);
call add_order_item(3, 5, 1);
call add_order_item(6, 14, 1);
call add_order_item(9, 35, 3);
call add_order_item(4, 27, 2);
call add_order_item(2, 45, 1);
call add_order_item(8, 59, 2);
call add_order_item(3, 10, 3);
call add_order_item(7, 22, 1);
call add_order_item(1, 52, 2);
call add_order_item(5, 37, 1);
call add_order_item(10, 66, 3);
