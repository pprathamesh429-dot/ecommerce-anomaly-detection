CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    region VARCHAR(50),
    age INTEGER,
    gender VARCHAR(20),
    signup_date DATE
);


CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(12,2)
);


CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    order_date DATE,
    quantity INTEGER,
    unit_price NUMERIC(12,2),
    discount NUMERIC(5,4),
    sales NUMERIC(14,2),
    order_status VARCHAR(20),

    CONSTRAINT fk_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);