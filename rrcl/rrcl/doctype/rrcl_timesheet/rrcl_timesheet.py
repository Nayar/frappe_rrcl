# Copyright (c) 2026, LEFINTECH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_timedelta

class RRCLTimesheet(Document):
	@frappe.whitelist()
	def generate_present(self):
		# self.table_employees = []
		attendance_records = frappe.get_all(
			"RRCL Attendance Record",
			filters={
				"date": self.date,
				"work_site": self.work_site
			},
			fields=["employee","time","date"] # Add the fields you need
		)


		summary = {}

		# 1. Load existing table into dictionary
		for row in self.get("table_employees"):
			summary[row.employee] = {
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
			
			if emp_id not in summary:
				summary[emp_id] = {
					"employee": emp_id,
					"status": "Working",
					"time_in": log_time,
					"time_out": log_time
				}
			else:
				curr = summary[emp_id]
				# Now both are timedeltas, so < and > will work
				if log_time < curr["time_in"]: 
					curr["time_in"] = log_time
				if log_time > curr["time_out"]: 
					curr["time_out"] = log_time

		# 3. Clear and Rebuild
		# self.set_value("table_employees", [])
		self.table_employees = []
		for data in summary.values():
			self.append("table_employees", data)