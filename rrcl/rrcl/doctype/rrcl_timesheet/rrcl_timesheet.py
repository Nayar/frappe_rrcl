# Copyright (c) 2026, LEFINTECH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_timedelta

class RRCLTimesheet(Document):
	def validate(self):
		duplicate = frappe.db.exists("RRCL Timesheet", {
			"date": self.date,
			"name": ["!=", self.name]
		})
		if duplicate:
			frappe.throw("A timesheet entry already exists for this date.")

		status_counts = {}
		for data in self.table_employees:
			current_status = data.get("status")
			if current_status:
				status_counts[current_status] = status_counts.get(current_status, 0) + 1
		self.summary = "\n".join([f"{status}: {count}" for status, count in status_counts.items()])

	@frappe.whitelist()
	def generate_present(self):
		active_employees = frappe.get_all(
			"RRCL Employee", 
			filters={"is_active": 1}, 
			fields=["name","default_worksite","attendance_type"]
		)

		summary = {}

		# 2. Initialize the summary with "Not Clocked" status
		for emp in active_employees:
			summary[emp.name] = {
				"employee": emp.name,
				"status": "Not clocked" if emp.attendance_type == "Digital" else "Working",
				"time_in": None,
				"time_out": None,
				"work_site": emp.default_worksite
			}

		attendance_records = frappe.get_all(
			"RRCL Attendance Record",
			filters={
				"date": self.date
			},
			fields=["employee","time","date","work_site"] # Add the fields you need
		)

		# 1. Load existing table into dictionary
		for row in self.get("table_employees"):
			summary[row.employee] = {
				"work_site" : row.work_site,
				"employee": row.employee,
				"status": row.status,
				# Ensure existing values are timedeltas for comparison
				"time_in": get_timedelta(row.time_in),
				"time_out": get_timedelta(row.time_out)
			}

		# 2. Process attendance_records
		for row in attendance_records:
			emp_id = row.employee
			
			# Convert incoming row.time to timedelta immediately
			log_time = get_timedelta(row.time)
			
			# Skip protected statuses
			if emp_id in summary and summary[emp_id]["status"] in ["Absent", "Local Leave"]:
				continue
			
			summary[emp_id] = {
				"employee": emp_id,
				"status": "Working",
				"work_site": row.work_site,
				"time_in": log_time,
				"time_out": log_time
			}

		# 3. Clear and Rebuild
		# self.set_value("table_employees", [])
		self.table_employees = []
		for data in summary.values():
			self.append("table_employees", data)
		self.save()
		self.generate_site_timesheets()

	def generate_site_timesheets(self):
		work_sites = frappe.get_all(
			"RRCL Work Site",
			fields=["name"]
		)
		
		for site in work_sites:
			# 1. Define the search criteria
			filters = {
				"work_site": site.name,
				"date": self.date
			}
			
			# 2. Check if it exists
			existing_name = frappe.db.exists("RRCL Site Timesheet", filters)

			if not existing_name:
				# Create new doc object
				site_timesheet = frappe.get_doc({
					"doctype": "RRCL Site Timesheet",
					"parent_timesheet": self.name,
					**filters # Unpacks work_site and date into the dict
				})
				site_timesheet.insert(ignore_permissions=True)
			else:
				# Fetch existing doc object
				site_timesheet = frappe.get_doc("RRCL Site Timesheet", existing_name)

			# 3. Update the Child Table
			site_timesheet.set("table_employees", []) # Clear existing rows safely
			
			for row in self.table_employees:
				# Logic Note: You might want an 'if row.site == site.name:' filter here
				# try:
					if row.work_site == site.name:
						site_timesheet.append("table_employees", {
							"employee": row.employee,
							"status": row.status,
							"time_in": row.time_in,
							"time_out": row.time_out
						})
				# except:
					pass
			# 4. Save the changes (updates existing or newly inserted doc)
			site_timesheet.save(ignore_permissions=True)
		
		frappe.db.commit() # Ensure changes are written if running from a custom button