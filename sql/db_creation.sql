--Create DataBase
create database TrainTickets
go
use TrainTickets
go

--Create tables
create table Companies(
[id] int not null primary key identity(0, 1),
[name] varchar(max) not null,
[phone] varchar(max) null
)
go
create table Trains(
[id] int not null primary key identity(0, 1),
[owner] int not null foreign key references Companies(id),
[type_1_seats] int not null,
[type_2_seats] int not null,
[type_3_seats] int not null
)
go
create table Cities(
[id] int not null primary key identity(0, 1),
[name] varchar(max) not null,
[longitude] int not null,
[latitude] int not null
)
go
create table Trips(
[id] int not null primary key identity(0, 1),
[train] int not null foreign key references Trains([id]),
[from_city] int not null foreign key references Cities([id]),
[to_city] int not null foreign key references Cities([id]),
[time] time not null,
[date] date not null,
[travel_time] int not null,
[seat_type_1_price] int not null,
[seat_type_2_price] int not null,
[seat_type_3_price] int not null
)
go
create table Tickets(
[id] int not null primary key identity(0, 1),
[trip_id] int not null foreign key references Trips([id]),
[seat_type] int not null,
[seat_num] int not null,
[status] int not null,
[book_date] date null,
[book_time] time null,
[first_name] varchar(max) null,
[last_name] varchar(max) null,
[card] varchar(max) null
)
go

create table SoldProviderTickets(
[id] int not null,
[trip_id] int not null,
[book_date] date null,
[book_time] time null,
[first_name] varchar(max) not null,
[last_name] varchar(max) not null,
[card] varchar(max) not null,
[provider_id] int not null
)
go

create view [dbo].[TicketsInfo] as
select
Tickets.[id] as 'id',
Trips.[date] as 'date',
Trips.[time] as 'time',
cf.[name] as 'from_city',
ct.[name] as 'to_city',
Trips.[travel_time] as 'travel_time',
Tickets.[seat_type] as 'seat_type',
Tickets.[seat_num] as 'seat_num',
case
	when Tickets.[seat_type] = 1 then Trips.[seat_type_1_price]
	when Tickets.[seat_type] = 2 then Trips.[seat_type_2_price]
	when Tickets.[seat_type] = 3 then Trips.[seat_type_3_price]
end as 'cost',
Trips.[id] as 'trip_id'
from Tickets
left join Trips on Trips.[id] = Tickets.[trip_id]
left join Cities as cf on cf.[id] = Trips.[from_city]
left join Cities as ct on ct.[id] = Trips.[to_city]
where Tickets.[status] = 0
go