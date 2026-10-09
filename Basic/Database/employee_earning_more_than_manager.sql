CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(50),
  salary NUMERIC(10,2),
  manager_id INT,
  FOREIGN KEY (manager_id) REFERENCES employees(id)
);


INSERT INTO employees (id, name, salary, manager_id) VALUES (1,"Krish",20000,NULL),(2,"Karan",30000,1),(3,"Kapil",50000,1),(4,"Kunal",15000,2);

SELECT e.name 
FROM employees e 
JOIN employees m 
ON e.manager_id = m.id 
WHERE e.salary>m.salary 
ORDER BY e.name;