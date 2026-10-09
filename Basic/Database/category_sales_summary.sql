CREATE TABLE categories (
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE products (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT REFERENCES categories(id),
    price NUMERIC(10, 2) NOT NULL
);

CREATE TABLE order_items (
    order_id INT,
    product_id INT REFERENCES products(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO categories (id, name) VALUES
(1, 'Electronics'),
(2, 'Clothing'),
(3, 'Books'),
(4, 'Furniture'),
(5, 'Sports');

INSERT INTO products (id, name, category_id, price) VALUES
(101, 'Laptop', 1, 800.00),
(102, 'Headphones', 1, 150.00),
(103, 'T-Shirt', 2, 25.00),
(104, 'Jeans', 2, 50.00),
(105, 'SQL Book', 3, 40.00),
(106, 'Python Book', 3, 60.00),
(107, 'Office Chair', 4, 300.00),
(108, 'Desk', 4, 500.00),
(109, 'Football', 5, 30.00),
(110, 'Tennis Racket', 5, 120.00);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 101, 2),
(1, 102, 3),
(2, 101, 1),
(2, 103, 10),
(2, 104, 5),
(3, 105, 8),
(3, 106, 10),
(4, 107, 2),
(4, 108, 2),
(5, 109, 10),
(5, 110, 8);

SELECT
    c.name AS category_name,
    SUM(oi.quantity) AS total_quantity_sold,
    ROUND(SUM(p.price * oi.quantity), 2) AS total_revenue
FROM categories c
JOIN products p
    ON c.id = p.category_id
JOIN order_items oi
    ON p.id = oi.product_id
GROUP BY c.id, c.name
HAVING SUM(p.price * oi.quantity) > 1000
ORDER BY total_revenue DESC;