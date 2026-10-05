# HRMS ER Diagram

```mermaid
erDiagram

    DEPARTMENT ||--o{ EMPLOYEE : contains
    EMPLOYEE ||--o{ ATTENDANCE : records
    EMPLOYEE ||--o{ LEAVE : requests
    EMPLOYEE ||--o{ PAYROLL : receives

    USER {
        int id PK
        varchar username
        varchar email
        varchar password
        varchar role
        boolean is_active
        timestamp created_at
    }

    DEPARTMENT {
        int id PK
        varchar name
        text description
    }

    EMPLOYEE {
        int id PK
        varchar employee_code UK
        varchar name
        varchar email UK
        varchar phone
        int department_id FK
        date joining_date
        varchar status
    }

    ATTENDANCE {
        int id PK
        int employee_id FK
        date attendance_date
        time check_in
        time check_out
        varchar status
    }

    LEAVE {
        int id PK
        int employee_id FK
        varchar leave_type
        date start_date
        date end_date
        text reason
        varchar status
    }

    PAYROLL {
        int id PK
        int employee_id FK
        date pay_period
        decimal basic_salary
        decimal allowances
        decimal deductions
        decimal net_salary
        varchar payment_status
    }