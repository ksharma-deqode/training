CREATE TABLE departments (
  id INT PRIMARY KEY, 
  name VARCHAR(50)
);

CREATE TABLE employees (
  id INT PRIMARY KEY, 
  name VARCHAR(50), 
  department_id INT,
  FOREIGN KEY (department_id) REFERENCES departments(id)

);

INSERT INTO departments (id, name)
VALUES
    (1, 'Engineering'),
    (2, 'HR'),
    (3, 'Finance'),
    (4, 'Marketing'),
    (5, 'Sales');


    INSERT INTO employees (id, name, department_id)
VALUES
    (1, 'Alice', 1),
    (2, 'Bob', 1),
    (3, 'Charlie', 2),
    (4, 'David', 2),
    (5, 'Emma', 2),
    (6, 'Frank', 2),
    (7, 'Grace', 4),
    (8, 'Henry', 4),
    (9, 'Ivy', 4),
    (10, 'Jack', 4),
    (11, 'Karen', 1),
    (12, 'Leo', 2);

SELECT 
d.name AS department_name
FROM departments d
LEFT JOIN employees e ON
d.id = e.department_id
WHERE e.id IS NULL
ORDER BY d.name;