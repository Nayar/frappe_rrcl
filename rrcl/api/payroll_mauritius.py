import requests
import frappe

class PayrollMauritius:
    @staticmethod
    def _get_token():
        """Fetch Procore token from RRCL Settings"""
        settings = frappe.get_single("RRCL Settings")   # Gets single doctype entry
        if not settings.payroll_mauritius_api_token:
            frappe.throw("❗ Payroll Mauritius Token missing in RRCL Settings")
        return settings.get_password("payroll_mauritius_api_token")

    @staticmethod
    def fetch_employees():
        employees_pm = requests.get(f"https://payrollmauritius.com/external/api/employees?token={PayrollMauritius._get_token()}&start=2025-01-01&end=2025-12-31").json()
        for epm in employees_pm:
            # print(epm)
            data = {
                "employee_code": epm.get("code"),
                "first_name": epm.get("firstname"),
                "last_name": epm.get("lastname"),
                "date_joined": epm.get("date_joined"),
                "date_left" : epm.get("departure_date"),
                "is_mauritian" : epm.get("mauritian"),
                "nic": epm.get("nic")
            }

            existing_name = frappe.db.get_value(
                "RRCL Employee",
                {"employee_code": data["employee_code"]},
                "name"
            )

            if existing_name:
                # Update existing employee
                # print("updating", data)
                rrcl_employee = frappe.get_doc("RRCL Employee", existing_name)
                rrcl_employee.update(data)
            else:
                # Create new employee
                # print("creating", data)
                rrcl_employee = frappe.get_doc({
                    "doctype": "RRCL Employee",
                    **data
                })
            rrcl_employee.save()
            frappe.db.commit()
            print('OK')

def sync_employees():
    frappe.logger().info("cron.... sync_employees start")   # logs to worker.log
    """Can be called from client side or list view"""
    PayrollMauritius.fetch_employees()
    print("cron job payroll")
    frappe.logger().info("cron.... sync_employees end")   # logs to worker.log
