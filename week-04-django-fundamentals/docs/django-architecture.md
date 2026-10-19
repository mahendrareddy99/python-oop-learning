# Django Architecture

## 1. Introduction

Django is a Python web framework used to build web applications and backend systems.

In the Enterprise HRMS Backend project, Django is used as the main backend framework. It provides project structure, URL routing, views, models, database integration, and application configuration.

---

## 2. Django Project Structure

The Day 1 Django project contains the following structure:

```text
week-03-django-fundamentals/
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ manage.py
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ config/
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ __init__.py
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ settings.py
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ urls.py
Ã¢â€â€š   Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ asgi.py
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ wsgi.py
Ã¢â€â€š
Ã¢â€Å“Ã¢â€â‚¬Ã¢â€â‚¬ docs/
Ã¢â€â€š   Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ django-architecture.md
Ã¢â€â€š
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬ requirements.txt
