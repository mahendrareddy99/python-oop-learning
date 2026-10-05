class ReportService:

    @staticmethod
    def generate_employee_report(employees):
        if not employees:
            return "No employees available."

        report = []
        report.append("=" * 50)
        report.append("         EMPLOYEE MANAGEMENT REPORT")
        report.append("=" * 50)

        for employee in employees:
            report.append(f"Employee ID : {employee.employee_id}")
            report.append(f"Name        : {employee.name}")
            report.append(f"Department  : {employee.department}")
            report.append(f"Salary      : {employee.calculate_salary():.2f}")
            report.append(f"Bonus       : {employee.calculate_bonus():.2f}")
            report.append("-" * 50)

        report.append(f"Total Employees: {len(employees)}")

        return "\n".join(report)