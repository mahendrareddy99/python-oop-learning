# HRMS Employee API Flow

## Overview

The Employee API follows this architecture:

Client -> API Endpoint -> Serializer -> API View -> Django ORM -> PostgreSQL

---

## Request Flow

```text
Client
   |
   v
HTTP Request
   |
   v
Django URL Routing
   |
   v
APIView
   |
   v
EmployeeSerializer
   |
   v
Validation
   |
   v
Django ORM
   |
   v
PostgreSQL
   |
   v
HTTP Response
   |
   v
Client