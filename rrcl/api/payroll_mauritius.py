import requests
import frappe

class PayrollMauritius:
    @staticmethod
    def fetch_employees():
        employees_pm = requests.get("https://payrollmauritius.com/external/api/employees?token=K6C3D52FQX6SP8pGroct8om8Jo6VebmA&start=2025-01-01&end=2025-12-31").json()
        for epm in employees_pm:
            # print(epm)
            data = {
                "employee_code": epm.get("code"),
                "first_name": epm.get("firstname"),
                "last_name": epm.get("lastname"),
                "date_joined": epm.get("date_joined")
            }

            existing_name = frappe.db.get_value(
                "RRCL Employee",
                {"employee_code": data["employee_code"]},
                "name"
            )

            if existing_name:
                # Update existing employee
                print("updating", data)
                rrcl_employee = frappe.get_doc("RRCL Employee", existing_name)
                rrcl_employee.update(data)
            else:
                # Create new employee
                print("creating", data)
                rrcl_employee = frappe.get_doc({
                    "doctype": "RRCL Employee",
                    **data
                })
            rrcl_employee.save()
            frappe.db.commit()
            print('OK')



PayrollMauritius.fetch_employees()