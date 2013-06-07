drop table if exists city;
drop table if exists zip;
create table city (
    id integer primary key,
    city text,
    state text,
    lat real,
    lng real,
    timezone text
);
create index city_name on city(city);
create table zip (
    id integer primary key,
    zip text,
    city_id integer,
    lat real,
    lng real,
    timezone text,
    foreign key(city_id) references city(id)
);

