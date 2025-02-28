-- Create tables
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    department VARCHAR(100) NOT NULL
);

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job VARCHAR(100) NOT NULL
);

-- Create 'employees' table
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    datetime VARCHAR(50) NOT NULL,
    department_id INT,
    job_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (job_id) REFERENCES jobs(id)
);