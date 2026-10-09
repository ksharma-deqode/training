CREATE TABLE students (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE courses (
    id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE enrollments (
    student_id INT REFERENCES students(id),
    course_id INT REFERENCES courses(id),
    PRIMARY KEY (student_id, course_id)
);

INSERT INTO students (id, name) VALUES
(1, 'Amit'),
(2, 'Priya'),
(3, 'Rahul'),
(4, 'Sneha'),
(5, 'Vikram');

INSERT INTO courses (id, title) VALUES
(101, 'Python Programming'),
(102, 'Database Management'),
(103, 'Web Development'),
(104, 'Data Structures');

INSERT INTO enrollments (student_id, course_id) VALUES
(1, 101),
(1, 102),
(2, 103),
(3, 101),
(3, 104),
(5, 102),
(5, 103);

SELECT
    s.id AS student_id,
    s.name AS student_name,
    c.title AS course_title
FROM students s
LEFT JOIN enrollments e
    ON s.id = e.student_id
LEFT JOIN courses c
    ON e.course_id = c.id
ORDER BY
    s.id ASC,
    e.course_id ASC;