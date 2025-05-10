create database Stocks


create table Company
(
CompanyName varchar(40),
RealName varchar(100),
Primary key (CompanyName)
);

create table PricesFDX
(
PriceID int identity(1,1),
CompanyName varchar(40),
PriceDate date,
OpenPrice decimal(6,2),
HighPrice decimal(6,2),
LowPrice decimal(6,2),
ClosePrice decimal(6,2),
Primary key (PriceID),
Foreign key (CompanyName) references Company(CompanyName)
);

create table PricesUPS
(
PriceID int identity(1,1),
CompanyName varchar(40),
PriceDate date,
OpenPrice decimal(6,2),
HighPrice decimal(6,2),
LowPrice decimal(6,2),
ClosePrice decimal(6,2),
Primary key (PriceID),
Foreign key (CompanyName) references Company(CompanyName)
);

create table PredictionsFDX
(
PricePredID int identity(1,1),
CompanyName varchar(40),
ds datetime,
trend float,
yhat_lower float,
yhat_upper float,
trend_lower float,
trend_upper float,
additive_terms float,
additive_terms_lower float,
additive_terms_upper float,
weekly float,
weekly_lower float,
weekly_upper float,
yearly float,
yearly_lower float,
yearly_upper float,
multiplicative_terms float,
multiplicative_terms_lower float,
multiplicative_terms_upper float,
yhat float,
Primary key (PricePredID),
Foreign key (CompanyName) references Company(CompanyName)
);

create table PredictionsUPS
(
PricePredID int identity(1,1),
CompanyName varchar(40),
ds datetime,
trend float,
yhat_lower float,
yhat_upper float,
trend_lower float,
trend_upper float,
additive_terms float,
additive_terms_lower float,
additive_terms_upper float,
weekly float,
weekly_lower float,
weekly_upper float,
yearly float,
yearly_lower float,
yearly_upper float,
multiplicative_terms float,
multiplicative_terms_lower float,
multiplicative_terms_upper float,
yhat float,
Primary key (PricePredID),
Foreign key (CompanyName) references Company(CompanyName)
);

create table PricesRiot
(
PriceID int identity(1,1),
CompanyName varchar(40),
PriceDate date,
OpenPrice decimal(6,2),
HighPrice decimal(6,2),
LowPrice decimal(6,2),
ClosePrice decimal(6,2),
Primary key (PriceID),
Foreign key (CompanyName) references Company(CompanyName)
);

create table PricesIntel
(
PriceID int identity(1,1),
CompanyName varchar(40),
PriceDate date,
OpenPrice decimal(6,2),
HighPrice decimal(6,2),
LowPrice decimal(6,2),
ClosePrice decimal(6,2),
Primary key (PriceID),
Foreign key (CompanyName) references Company(CompanyName)
);

create table PredictionsRiot
(
PricePredID int identity(1,1),
CompanyName varchar(40),
ds datetime,
trend float,
yhat_lower float,
yhat_upper float,
trend_lower float,
trend_upper float,
additive_terms float,
additive_terms_lower float,
additive_terms_upper float,
weekly float,
weekly_lower float,
weekly_upper float,
yearly float,
yearly_lower float,
yearly_upper float,
multiplicative_terms float,
multiplicative_terms_lower float,
multiplicative_terms_upper float,
yhat float,
Primary key (PricePredID),
Foreign key (CompanyName) references Company(CompanyName)
);

create table PredictionsIntel
(
PricePredID int identity(1,1),
CompanyName varchar(40),
ds datetime,
trend float,
yhat_lower float,
yhat_upper float,
trend_lower float,
trend_upper float,
additive_terms float,
additive_terms_lower float,
additive_terms_upper float,
weekly float,
weekly_lower float,
weekly_upper float,
yearly float,
yearly_lower float,
yearly_upper float,
multiplicative_terms float,
multiplicative_terms_lower float,
multiplicative_terms_upper float,
yhat float,
Primary key (PricePredID),
Foreign key (CompanyName) references Company(CompanyName)
);


INSERT INTO Company VALUES ('INTC.NE','Intel Corporation'),('RIOT', 'Riot Platforms, Inc.');
INSERT INTO Company VALUES ('FDX','FedEx Corporation'),('UPS', 'United Parcel Service, Inc.');

