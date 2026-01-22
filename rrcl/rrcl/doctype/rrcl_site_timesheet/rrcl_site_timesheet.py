# Copyright (c) 2026, LEFINTECH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RRCLSiteTimesheet(Document):
	def on_submit(self):
		parent_timesheet = frappe.get_doc("RRCL Timesheet", self.parent_timesheet)

		count = 0
		for row in self.table_employees:
			for parent_row in parent_timesheet.table_employees:
				if(row.employee == parent_row.employee and parent_row.status != row.status):
					parent_row.status = row.status
					count += 1
		if(count > 0):
			parent_timesheet.save()
