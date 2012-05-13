CREATE TABLE outputs (
    output_id serial PRIMARY KEY,
    output_name VARCHAR(50) NOT NULL,
    output_price INTEGER NOT NULL CHECK (output_price>10 AND output_price<1000000)
);
CREATE TABLE customers (
    customer_id serial PRIMARY KEY,
    address VARCHAR(50) NOT NULL,
    type BOOLEAN NOT NULL,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(25) NOT NULL,
    fax VARCHAR(25) NOT NULL,
    email VARCHAR(50) NOT NULL
);
CREATE TABLE customers_lp (
    customer_id INTEGER REFERENCES customers (customer_id) PRIMARY KEY,
    bank VARCHAR(50) NOT NULL,
    account INTEGER NOT NULL,
    bik INTEGER NOT NULL,
    inn INTEGER NOT NULL,
    okonh INTEGER NOT NULL,
    okpo INTEGER NOT NULL
);
CREATE TABLE delivery_diagrams (
    diagram_id serial PRIMARY KEY,
    vehicle VARCHAR(50) NOT NULL,
    agent VARCHAR(40) NOT NULL,
    plan_date DATE NOT NULL,
    fact_date TIMESTAMP,
    status BOOLEAN NOT NULL
);
CREATE TABLE delpoints (
    delpoint_id serial PRIMARY KEY,
    del_address VARCHAR(50) NOT NULL,
    zone VARCHAR(20) NOT NULL,
    floor VARCHAR(10) NOT NULL,
    elevator BOOLEAN NOT NULL,
    entrance VARCHAR(10),
    code VARCHAR(10)
);
CREATE TABLE orders (
    order_id serial PRIMARY KEY,
    diagram_id INTEGER REFERENCES delivery_diagrams (diagram_id),
    customer_id INTEGER REFERENCES customers (customer_id),
    delpoint_id INTEGER REFERENCES delpoints (delpoint_id),
    responsible VARCHAR(30) NOT NULL,
    order_date DATE NOT NULL,
    order_amount INTEGER NOT NULL CHECK (order_amount>10 AND order_amount<10000000),
    order_total INTEGER NOT NULL CHECK (order_total>10 AND order_total<10000000)
);
CREATE TABLE orders_outputs (
    order_id INTEGER REFERENCES orders(order_id),
    output_id INTEGER REFERENCES outputs(output_id),
    quantity INTEGER CHECK (quantity>0 AND quantity<200),
    discount INTEGER CHECK (discount>=0 AND discount<100000),
    PRIMARY KEY (order_id, output_id)
);


CREATE USER manager with password '123456';
grant select,insert on outputs,customers,customers_lp,orders_outputs,
                       orders,delpoints,delivery_diagrams to manager;
grant select,update on customers_customer_id_seq,delivery_diagrams_diagram_id_seq,
                       delpoints_delpoint_id_seq,orders_order_id_seq,outputs_output_id_seq to manager;
