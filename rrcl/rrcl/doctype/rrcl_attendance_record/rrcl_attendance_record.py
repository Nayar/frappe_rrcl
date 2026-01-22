# Copyright (c) 2025, LEFINTECH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


from frappe.utils import get_time

class RRCLAttendanceRecord(Document):
    def save(self):
        # 1. Get or Create Parent Timesheet
        timesheet_name = self.get_or_create_parent()
        parent_doc = frappe.get_doc("RRCL Site Timesheet", timesheet_name)
        
        # 2. Find if there's an open entry (Working status and no time_out)
        existing_row = None
        for row in parent_doc.table_employees:
            if row.employee == self.employee:
                existing_row = row
                break
        
        new_time = get_time(self.time)

        if not existing_row:
            # CREATE NEW: No open record found, so this is a "Clock In"
            parent_doc.append("table_employees", {
                "employee": self.employee,
                "status": "Working",
                "time_in": self.time
            })
            parent_doc.save(ignore_permissions=True)
            
        else:
            # UPDATE EXISTING: Logic for Clock Out
            time_in = get_time(existing_row.time_in)
            
            if new_time > time_in:
                # Normal Clock Out
                existing_row.time_out = self.time
                # Optional: existing_row.status = "Completed" 
                parent_doc.save(ignore_permissions=True)
            else:
                # Edge Case: The time provided is earlier than Time In
                existing_row.time_in = self.time
                # Optional: existing_row.status = "Completed" 
                parent_doc.save(ignore_permissions=True)
                # frappe.msgprint(f"Error: Time {self.time} is earlier than Time In ({existing_row.time_in})")

    def get_or_create_parent(self):
        filters = {"work_site": self.work_site, "date": self.date}
        name = frappe.db.exists("RRCL Site Timesheet", filters)
        if not name:
            doc = frappe.get_doc({"doctype": "RRCL Site Timesheet", **filters})
            doc.insert(ignore_permissions=True)
            return doc.name
        return name