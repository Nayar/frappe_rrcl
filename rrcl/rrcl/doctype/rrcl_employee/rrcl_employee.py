# Copyright (c) 2025, LEFINTECH LTD and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from datetime import date
from frappe.utils.data import getdate


class RRCLEmployee(Document):
	def before_save(self):
		print("before save")
		self.full_name = f"{self.first_name} {self.last_name} ({self.employee_code})"
		print(self.date_left)
		if getattr(self, "date_left", None):
			# Convert to date if it's a string
			print("testing", self)
			left_date = getdate(self.date_left) if isinstance(self.date_left, str) else self.date_left
			self.is_active = left_date > date.today()
			print("inactive", self)
		else:
			self.is_active = True