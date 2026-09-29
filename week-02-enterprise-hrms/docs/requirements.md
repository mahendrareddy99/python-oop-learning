# Employee Management System — Requirements

## 1. Introduction

The Employee Management System is a core module of an Enterprise Human Resource Management System (HRMS).

The system will allow HR personnel and authorized users to manage employee information, employee accounts, and employee status through a backend application.

The future backend will be implemented using:

- Python
- Django
- Django REST Framework
- PostgreSQL

---

## 2. What is a System?

A system is a collection of components that work together to achieve a specific business or technical objective.

For an HRMS, the major components may include:

- Client application
- API
- Backend application
- Database
- Authentication system

These components communicate with each other to provide HR functionality.

---

## 3. What is Software Architecture?

Software architecture describes the high-level structure of a software system.

It defines:

- Major components
- Responsibilities of components
- Communication between components
- Data flow
- Technology choices
- System boundaries

For this HRMS, the architecture will eventually contain:

```text
Client
   |
   v
REST API
   |
   v
Django Backend
   |
   v
PostgreSQL Database

---

# Day 2 — Requirements Engineering

## 4. What is Requirements Engineering?

Requirements engineering is the process of identifying, documenting,
analyzing, validating, and managing the requirements of a software system.

For the HRMS project, requirements help the development team understand
what the system should do and how the system should behave.

Requirements are mainly classified into:

1. Functional Requirements
2. Non-Functional Requirements

---

## 5. Functional Requirements

Functional requirements describe the features and operations that
the HRMS system must provide.

They answer the question:

> What should the system do?

Examples include:

- User login
- Employee creation
- Employee search
- Leave application
- Attendance recording
- Payroll processing
- Report generation

---

## 6. Non-Functional Requirements

Non-functional requirements describe the quality, performance,
security, reliability, and other characteristics of the system.

They answer the question:

> How should the system perform?

Examples include:

- Security
- Performance
- Availability
- Reliability
- Scalability
- Maintainability

---

# 7. HRMS Functional Requirements

## 7.1 Authentication

- The system shall allow users to log in using valid credentials.
- The system shall authenticate users before accessing protected resources.
- The system shall allow users to log out.
- The system shall support role-based access control.
- The system shall reject invalid login credentials.

## 7.2 Employee Management

- HR users shall be able to add employees.
- HR users shall be able to view employee details.
- HR users shall be able to update employee information.
- HR users shall be able to deactivate employees.
- Users shall be able to search employees by employee ID or name.
- The system shall maintain employee employment status.

## 7.3 Department Management

- HR administrators shall be able to create departments.
- Users shall be able to view department details.
- HR administrators shall be able to update department information.
- The system shall allow employees to be associated with departments.
- The system shall prevent invalid department assignments.

## 7.4 Attendance

- Employees shall be able to record check-in time.
- Employees shall be able to record check-out time.
- Employees shall be able to view attendance records.
- HR users shall be able to view employee attendance.
- The system shall calculate attendance duration.

## 7.5 Leave Management

- Employees shall be able to submit leave requests.
- Employees shall be able to view their leave history.
- Managers shall be able to approve or reject leave requests.
- The system shall maintain employee leave balances.
- The system shall update leave balances after approved leave.

## 7.6 Payroll

- HR users shall be able to maintain employee salary information.
- The system shall calculate employee payroll.
- The system shall maintain payroll records.
- Employees shall be able to view their payroll information.
- HR users shall be able to generate payroll reports.

## 7.7 Recruitment

- Recruiters shall be able to create job openings.
- Recruiters shall be able to view job openings.
- Recruiters shall be able to add candidate information.
- Recruiters shall be able to update candidate status.
- The system shall track candidates through recruitment stages.

## 7.8 Assets

- Administrators shall be able to register company assets.
- Administrators shall be able to update asset information.
- Assets shall be assignable to employees.
- Users shall be able to view assets assigned to them.
- Administrators shall be able to update asset status.

## 7.9 Performance Management

- Managers shall be able to create employee performance reviews.
- Managers shall be able to record performance ratings.
- Employees shall be able to view their performance information.
- The system shall maintain employee performance history.

## 7.10 Notifications

- The system shall send notifications for important HR events.
- Employees shall receive notifications about leave decisions.
- Employees shall receive relevant attendance notifications.
- Employees shall receive relevant payroll notifications.
- Users shall be able to view notification history.

## 7.11 Reports

- HR users shall be able to generate employee reports.
- The system shall provide attendance reports.
- The system shall provide leave reports.
- The system shall provide payroll reports.
- Reports shall support filtering by relevant criteria.

## 7.12 Audit Logs

- The system shall record important user actions.
- Audit logs shall contain the user who performed the action.
- Audit logs shall contain the action and timestamp.
- Authorized administrators shall be able to view audit logs.
- The system shall support searching audit records.

---

# 8. Non-Functional Requirements

## 8.1 Security

- The system shall protect sensitive employee information.
- Protected resources shall require authentication and authorization.
- Passwords shall be securely hashed.
- Role-based access control shall be implemented.
- Unauthorized users shall not be allowed to access restricted resources.

## 8.2 Performance

- The system should provide timely responses for normal requests.
- Database queries should be optimized for frequently accessed data.
- The system should support multiple concurrent users.

## 8.3 Availability

- The system should be available during normal business operations.
- The system should recover from temporary service failures.

## 8.4 Reliability

- Employee and HR data should not be lost during normal operations.
- Database transactions should maintain data consistency.
- System failures should be logged for troubleshooting.

## 8.5 Scalability

- The system should support an increasing number of employees.
- The backend should support increasing request volume.
- The database design should support future growth.

## 8.6 Maintainability

- The application should follow a modular architecture.
- The codebase should follow consistent coding standards.
- APIs and major components should be documented.
- Automated tests should be maintained.

---

# 9. Requirements Classification

| Module | Functional Requirements | Non-Functional Requirements |
|---|---|---|
| Authentication | Login, logout, authentication, role management | Security, performance |
| Employee Management | Add, view, update, deactivate, search | Security, reliability |
| Department Management | Create, view, update departments | Security, consistency |
| Attendance | Check-in, check-out, attendance records | Reliability, accuracy |
| Leave | Apply, approve, reject, leave balance | Security, consistency |
| Payroll | Salary and payroll processing | Security, accuracy, reliability |
| Recruitment | Jobs, candidates, recruitment stages | Security, scalability |
| Assets | Register, assign, update assets | Security, reliability |
| Performance | Reviews, ratings, history | Security, consistency |
| Notifications | Send and view notifications | Performance, reliability |
| Reports | Generate and filter reports | Performance, accuracy |
| Audit Logs | Record and view system actions | Security, reliability |

---

# 10. Requirements Summary

The HRMS requirements define the features and quality attributes
needed to develop the system.

Functional requirements describe what the HRMS should do, such as
managing employees, attendance, leave, payroll, recruitment, and reports.

Non-functional requirements describe how the system should operate,
including security, performance, availability, reliability,
scalability, and maintainability.

These requirements will be used as a foundation for the future
Django, Django REST Framework, and PostgreSQL implementation.