--Create DataBase
create database TrainTickets
go
use TrainTickets
go

--Create tables
create table Companies(
[Id] int not null primary key identity(0, 1),
[Name] varchar(max) not null,
[Phone] varchar(max) null
)
go
create table Trains(
[Id] int not null primary key identity(0, 1),
[Owner] int not null foreign key references Companies(Id),
[Type1Seats] int not null,
[Type2Seats] int not null,
[Type3Seats] int not null
)
go
create table Cities(
[Id] int not null primary key identity(0, 1),
[Name] varchar(max) not null,
[Longitude] int not null,
[Latitude] int not null
)
go
create table Trips(
[Id] int not null primary key identity(0, 1),
[Train] int not null foreign key references Trains(Id),
[CityFrom] int not null foreign key references Cities(Id),
[CityFromTime] time not null,
[CityFromDate] date not null,
[TravelTime] int not null,
[CityTo] int not null foreign key references Cities(Id),
[Type1Price] int not null,
[Type2Price] int not null,
[Type3Price] int not null
)
go
create table Tickets(
[Id] int not null primary key identity(0, 1),
[Trip] int not null foreign key references Trips(Id),
[Type] int not null,
[SeatNum] int not null,
[Status] int not null,
[BookDate] date null,
[BookTime] time null,
[FirstName] varchar(max) null,
[LastName] varchar(max) null,
[CardNumber] varchar(max) null
)
go
create view [dbo].[TicketsInfo] as
select
Tickets.[Id] as 'id',
Trips.[CityFromDate] as 'date',
Trips.[CityFromTime] as 'time',
cf.[Name] as 'from_city',
ct.[Name] as 'to_city',
Trips.[TravelTime] as 'travel_time',
Tickets.[Type] as 'seat_type',
Tickets.[SeatNum] as 'seat_num',
case
	when Tickets.[Type] = 1 then Trips.Type1Price
	when Tickets.[Type] = 2 then Trips.Type2Price
	when Tickets.[Type] = 3 then Trips.Type3Price
end as 'cost',
Trips.[Id] as 'trip_id'
from Tickets
left join Trips on Trips.[Id] = Tickets.[Trip]
left join Cities as cf on cf.[Id] = Trips.[CityFrom]
left join Cities as ct on ct.[Id] = Trips.[CityTo]
go