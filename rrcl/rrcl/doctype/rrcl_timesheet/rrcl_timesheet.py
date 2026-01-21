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

	@frappe.whitelist()
	def generate_present(self):
		active_employees = frappe.get_all(
			"RRCL Employee", 
			filters={"is_active": 1}, 
			fields=["name"]
		)

		summary = {}

		# 2. Initialize the summary with "Not Clocked" status
		for emp in active_employees:
			summary[emp.name] = {
				"employee": emp.name,
				"status": "Not clocked",
				"work_site": None,
				"time_in": None,
				"time_out": None
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