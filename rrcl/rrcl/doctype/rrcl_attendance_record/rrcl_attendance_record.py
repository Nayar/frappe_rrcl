
import frappe

from frappe.model.document import Document

from frappe.utils import get_time

class RRCLAttendanceRecord(Document):

	def after_insert(self):
		self.update_min_max_time()
	def update_min_max_time(self):
		timesheet_name = self.get_or_create_parent()

		# Get earliest and latest swipe times for this employee/day/site
		result = frappe.db.sql("""
			SELECT
				MIN(time) AS min_time,
				MAX(time) AS max_time
			FROM `tabRRCL Attendance Record`
			WHERE employee = %s
			AND work_site = %s
			AND date = %s
		""", (self.employee, self.work_site, self.date), as_dict=True)[0]

		min_time = result.min_time
		max_time = result.max_time

		# Get or create child row
		row_name = frappe.db.get_value(
			"RRCL Site Timesheet Details",
			{
				"parent": timesheet_name,
				"employee": self.employee
			},
			"name"
		)

		if not row_name:
			# Create once
			parent_doc = frappe.get_doc("RRCL Site Timesheet", timesheet_name)
			parent_doc.append("table_employees", {
				"employee": self.employee,
				"time_in": min_time,
				"time_out": max_time if min_time != max_time else None
			})
			parent_doc.save(ignore_permissions=True)

		else:
			# Update deterministically
			frappe.db.set_value(
				"RRCL Site Timesheet Details",
				row_name,
				{
					"time_in": min_time,
					"time_out": max_time if min_time != max_time else None
				}
			)



	def get_or_create_parent(self):
		filters = {"work_site": self.work_site, "date": self.date}
		name = frappe.db.get_value("RRCL Site Timesheet", filters)
		if not name:
			doc = frappe.get_doc({"doctype": "RRCL Site Timesheet", **filters})
			doc.insert(ignore_permissions=True)
			return doc.name
		return name

	
