# Copyright (c) 2026, LEFINTECH LTD and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import csv
import frappe
from frappe.utils.file_manager import get_file_path
from datetime import datetime


class RRCLHIKVisionAttendanceUpload(Document):
    def before_save(self):
        self.process_csv()

    @frappe.whitelist()
    def process_csv(self):
        if not self.attach_mvjs:
            frappe.throw("Please attach a CSV file first.")

        # 1. Get the file path from the attachment URL
        file_path = get_file_path(self.attach_mvjs)
        
        count = 0
        headers_found = False

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            for row in reader:
                # Logic: Skip lines until header is found
                if not headers_found:
                    if row[:5] == ['First Name', 'Last Name', 'ID', 'Department', 'Date']:
                        headers_found = True
                    continue

                # Skip empty or malformed rows
                if len(row) < 13:
                    continue
                print(row)
                extra_fields = len(row) - 13
                name_parts = row[:1 + extra_fields]  # include extra parts in first name
                last_name = row[1 + extra_fields]
                rest = row[2 + extra_fields:]
                
                first_name = " ".join(part.strip() for part in name_parts if part.strip())
                device_serial_no_short = rest[7].strip()
                employee_code = rest[0].strip()

                try:
                    # Parse Date and Time
                    date_obj = datetime.strptime(rest[2], "%d-%m-%Y").date()
                    time_obj = datetime.strptime(rest[3], "%H:%M").time()

                    equipment_id = frappe.db.get_value("RRCL Equipment", 
                        {"serial_number": ["like", f"%{device_serial_no_short}"]}, 
                        "name"
                    )
                    print(f"checking {employee_code}")
                    if not frappe.db.exists("RRCL Employee", {"employee_code" : employee_code}):
                        print(f"creating {employee_code}")
                        new_employee = frappe.get_doc({
                            "doctype": "RRCL Employee",
                            "employee_code" : employee_code,
                            "first_name" : first_name,
                            "last_name" : last_name
                        })
                        print(f"created {employee_code}")
                        frappe.msgprint(f"Creating employee {new_employee}")
                        new_employee.insert(ignore_permissions=True)
                        # frappe.db.commit()


                    equipment_doc = frappe.get_doc("RRCL Equipment", equipment_id)
                    work_site = equipment_doc.assigned_to

                    # 2. Create the child record (RRCL Attendance Record)

                    obj = {
                        "doctype": "RRCL Attendance Record",
                        "employee": employee_code, # Linking to Employee ID
                        "date": date_obj,
                        "time": time_obj,
                        "work_site": work_site, # Mapping 'Location' to 'Work Site'
                        "device_serial_number": rest[7].strip(),
                        # Add other fields as per your Doctype
                    }
                    if not frappe.db.exists("RRCL Attendance Record", obj):
                        attendance = frappe.get_doc(obj)
                        attendance.insert(ignore_permissions=True)
                        attendance.save()
                    else:
                        frappe.msgprint("Record already exists, skipping...")
                    count += 1

                except Exception as e:
                    # Log error in Frappe Error Log instead of printing to console
                    frappe.log_error(message=f"Row Error: {str(e)}", title="HIK Upload Error")
                    frappe.msgprint(f'message=f"Row Error: {str(e)}" {obj}')
                    continue

            frappe.msgprint(f'Imported {count} attendance records successfully.')