INSERT into outputs(output_name,output_price)
values ('HTC Sensation',17400),
('HTC Desire S',12590),
('HTC Wildfire S',7840),
('HTC Incredible S',14169),
('Samsung Galaxy Ace S5830',8850),
('Samsung Galaxy Nexus I9250',23450),
('Sony Ericsson Xperia ray',10690),
('HTC Explorer',6400),
('HTC Rhyme',15990),
('Samsung Galaxy Y S5360',5410),
('Samsung Galaxy S Plus I9001',14890),
('HTC EVO 3D',16990),
('Sony Ericsson Xperia arc S',15200),
('Samsung Galaxy Gio S5660',7200),
('Sony Ericsson Xperia neo V',10900),
('Samsung Galaxy W I8150',12390),
('Samsung Galaxy Mini S5570',5999),
('Sony Ericsson Live with Walkman',7800),
('Sony Ericsson Xperia X8',5831),
('HTC Salsa',9990);

INSERT into customers(address,type,name,phone,fax,email)
values ('Санкт-Петербург Невский пр. 30',true,'Ivanov Petr','123-12-34','123-12-34','ip@bk.ru'),
       ('Санкт-Петербург Невский пр. 36',true,'Petrov Ivan','145-45-56','566-56-56','pi@bk.ru'),
       ('Санкт-Петербург Коломяжский пр. 26',true,'Smirnov Ivan','145-45-56','566-56-56','kpi@bk.ru'),
       ('Санкт-Петербург Энгельса пр. 31',true,'Kotov Mike','145-45-56','566-56-56','pk@bk.ru'),
       ('Санкт-Петербург Вознесенский пр. 12',false,'ЗАО ФКП','923-12-35','923-12-35','fkp@list.ru'),
       ('Санкт-Петербург Главная ул. 5',false,'ОАО КБалт','623-16-64','623-16-64','kbalt@bk.ru');

INSERT into customers_lp(customer_id,bank,account,bik,inn,okonh,okpo)
values (5,'Уралсиб',90023466,20119917,28574592,34110040,12045300),
       (6,'Сбербанк',94026466,40619913,28475492,34140943,12094303);
       
INSERT into delivery_diagrams(vehicle,agent,plan_date,fact_date,status)
values ('в123во 178','23','2012-01-30','2012-01-30 12:20:00','true');

INSERT into delivery_diagrams(vehicle,agent,plan_date,status)
values ('в123во 178','12','2012-06-13','false'),
       ('в124во 178','12','2012-02-13','false'),
       ('в124во 178','12','2012-05-23','false'),
       ('в124во 178','12','2012-05-16','false'),
       ('в124во 178','23','2012-06-14','false');
       
INSERT into delpoints(del_address,zone,floor,elevator,entrance,code)
values ('Санкт-Петербург Невский пр. 30','3','7',true,'3','2245'),
       ('Санкт-Петербург Коломяжский пр. 26','3','7',true,'3','2245'),
       ('Санкт-Петербург Невский пр. 31','3','7',true,'3','2245'),
       ('Москва Садовый пр. 30','3','7',true,'3','2245');

INSERT into delpoints(del_address,zone,floor,elevator)
values ('Санкт-Петербург Пушкина ул. 2','1','1',false),
       ('Санкт-Петербург Гоголя ул. 4','2','1',false);
       
INSERT into orders (diagram_id,customer_id,delpoint_id,responsible,
                    order_date,order_amount,order_total)
values (1,1,1,'Орлов М.С.','2012-04-13',7840,7640),
       (2,2,2,'Зотов Т.В.','2012-04-15',15680,15680),
       (3,3,3,'Зотов Т.В.','2012-04-11',22810,22800),
       (4,4,4,'Орлов М.С.','2012-04-12',10900,10900),
       (5,5,5,'Зотов Т.В.','2012-04-15',9990,9990),
       (6,6,6,'Зотов Т.В.','2012-04-17',21662,21662);
      
INSERT into orders_outputs (order_id,output_id,quantity,discount) values 
(1,3,1,200),
(2,2,3,0),
(3,1,1,0),
(3,10,1,10),
(4,15,1,0),
(5,20,1,0),
(6,19,2,0),
(6,20,1,0);