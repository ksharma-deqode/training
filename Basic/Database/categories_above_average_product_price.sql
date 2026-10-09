CREATE TABLE categories (
  id INT PRIMARY KEY, 
  name VARCHAR(20)

); 

CREATE TABLE products (
  id INT PRIMARY KEY, 
  name VARCHAR(50), 
  price DECIMAL(10,2), 
  category_id INT,
  FOREIGN KEY (category_id) REFERENCES categories(id)

);
INSERT INTO categories (id, name)
VALUES
    (1, 'Electronics'),
    (2, 'Clothing'),
    (3, 'Books'),
    (4, 'Furniture'),
    (5, 'Sports');
    
INSERT INTO products (id, name, price, category_id)
VALUES
    (1, 'Laptop',        75000.00, 1),
    (2, 'Smartphone',    45000.00, 1),
    (3, 'Headphones',     3500.00, 1),
    (4, 'Keyboard',       1800.00, 1),

    (5, 'T-Shirt',         799.00, 2),
    (6, 'Jeans',          1999.00, 2),
    (7, 'Jacket',         3499.00, 2),
    (8, 'Sneakers',       2999.00, 2),

    (9, 'Python Book',     899.00, 3),
    (10, 'SQL Book',       699.00, 3),
    (11, 'PostgreSQL Guide', 1299.00, 3),

    (12, 'Office Chair',  8500.00, 4),
    (13, 'Desk',         12000.00, 4),
    (14, 'Bookshelf',     6500.00, 4),

    (15, 'Football',       999.00, 5),
    (16, 'Cricket Bat',   2499.00, 5),
    (17, 'Tennis Racket', 3999.00, 5);


SELECT c.name AS category_name
FROM categories c
LEFT JOIN products p
ON c.id = p.category_id
GROUP BY c.id,c.name
HAVING AVG(p.price)> (
SELECT AVG(price) FROM products);