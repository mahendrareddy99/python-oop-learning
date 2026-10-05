# HRMS Database Design

## 1. Overview

The Enterprise HRMS database is designed to manage employee, department, attendance, leave, and payroll information.

The initial database consists of the following tables:

- User
- Employee
- Department
- Attendance
- Leave
- Payroll

The design follows a relational database structure using primary keys and foreign keys to establish relationships between entities.

---

## 2. Database Fundamentals

### Database

A database is an organized collection of structured information that can be stored, accessed, and managed efficiently.

### Table

A table stores data related to a specific entity.

### Row

A row represents one complete record in a table.

### Column

A column represents a specific attribute of a record.

### Primary Key

A primary key uniquely identifies each record in a table.

### Foreign Key

A foreign key references the primary key of another table and establishes a relationship between tables.

---

## 3. Database Relationships

### One-to-One

One record in one table is associated with one record in another table.

Example:

Employee 1 - 1 User

### One-to-Many

One record in one table can be associated with multiple records in another table.

Example:

Department 1 - N Employee

### Many-to-Many

Multiple records in one table can be associated with multiple records in another table.

A many-to-many relationship normally requires an intermediate table.

---

# 4. HRMS Tables

## 4.1 User

| Column | Data Type | Constraint | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique user ID |
| username | VARCHAR(100) | NOT NULL, UNIQUE | Login username |
| email | VARCHAR(150) | NOT NULL, UNIQUE | User email |
| password | VARCHAR(255) | NOT NULL | Hashed password |
| role | VARCHAR(50) | NOT NULL | User role |
| is_active | BOOLEAN | DEFAULT TRUE | Account status |
| created_at | TIMESTAMP | NOT NULL | Account creation time |

## 4.2 Department

| Column | Data Type | Constraint | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique department ID |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Department name |
| description | TEXT | NULL | Department description |

## 4.3 Employee

| Column | Data Type | Constraint | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique employee ID |
| employee_code | VARCHAR(50) | NOT NULL, UNIQUE | Unique employee code |
| name | VARCHAR(150) | NOT NULL | Employee full name |
| email | VARCHAR(150) | NOT NULL, UNIQUE | Employee email |
| phone | VARCHAR(20) | NULL | Employee phone number |
| department_id | Integer | Foreign Key | Employee department |
| joining_date | DATE | NOT NULL | Date employee joined |
| status | VARCHAR(30) | DEFAULT ACTIVE | Employment status |

Relationship:

Department 1 - N Employee

## 4.4 Attendance

| Column | Data Type | Constraint | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique attendance ID |
| employee_id | Integer | Foreign Key | Employee reference |
| attendance_date | DATE | NOT NULL | Attendance date |
| check_in | TIME | NULL | Employee check-in time |
| check_out | TIME | NULL | Employee check-out time |
| status | VARCHAR(30) | NOT NULL | Attendance status |

Relationship:

Employee 1 - N Attendance

## 4.5 Leave

| Column | Data Type | Constraint | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique leave ID |
| employee_id | Integer | Foreign Key | Employee reference |
| leave_type | VARCHAR(50) | NOT NULL | Type of leave |
| start_date | DATE | NOT NULL | Leave start date |
| end_date | DATE | NOT NULL | Leave end date |
| reason | TEXT | NULL | Reason for leave |
| status | VARCHAR(30) | DEFAULT PENDING | Leave request status |

Relationship:

Employee 1 - N Leave

## 4.6 Payroll

| Column | Data Type | Constraint | Description |
|---|---|---|---|
| id | Integer | Primary Key | Unique payroll ID |
| employee_id | Integer | Foreign Key | Employee reference |
| pay_period | DATE | NOT NULL | Payroll period |
| basic_salary | DECIMAL(12,2) | NOT NULL | Basic salary |
| allowances | DECIMAL(12,2) | DEFAULT 0 | Total allowances |
| deductions | DECIMAL(12,2) | DEFAULT 0 | Total deductions |
| net_salary | DECIMAL(12,2) | NOT NULL | Net salary |
| payment_status | VARCHAR(30) | DEFAULT PENDING | Payment status |

Salary calculation:

Gross Salary = Basic Salary + Allowances

Net Salary = Gross Salary - Deductions

---

# 5. HRMS Relationships

Department 1 - N Employee

Employee 1 - N Attendance

Employee 1 - N Leave

Employee 1 - N Payroll

---

# 6. Foreign Key Relationships

| Child Table | Foreign Key | Parent Table | Parent Key |
|---|---|---|---|
| Employee | department_id | Department | id |
| Attendance | employee_id | Employee | id |
| Leave | employee_id | Employee | id |
| Payroll | employee_id | Employee | id |

---

# 7. Database Constraints

The HRMS database uses:

- PRIMARY KEY
- FOREIGN KEY
- NOT NULL
- UNIQUE
- DEFAULT
- CHECK

Primary keys uniquely identify records.

Foreign keys maintain relationships between related tables.

NOT NULL ensures required fields contain a value.

UNIQUE prevents duplicate values.

DEFAULT provides a value when one is not supplied.

CHECK can prevent invalid values such as negative salary.

---

# 8. ER Diagram

The basic HRMS relationship is:

Department
    |
    | 1
    |
    | N
    |
Employee
    |
    +---- Attendance
    |
    +---- Leave
    |
    +---- Payroll

---

# 9. Design Summary

The HRMS database follows a relational database design.

Employee is the central business entity and is connected to Department, Attendance, Leave, and Payroll.

Foreign keys maintain relationships between the entities and help preserve referential integrity.

Primary keys uniquely identify records, while database constraints help maintain data quality.

This database design can later be implemented using Django Models and PostgreSQL.
