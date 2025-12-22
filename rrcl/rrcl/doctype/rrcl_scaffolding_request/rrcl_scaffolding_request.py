# Copyright (c) 2025, LEFINTECH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RRCLScaffoldingRequest(Document):
	def before_save(self):

		# Iterate through the child table rows (table_yngh)
		for row in self.table_yngh:
			print(row.item)
			stock_details = frappe.get_all(
				'RRCL Stock', 
				filters={'item': row.item}, 
				fields=['qty']
			)
			if(len(stock_details)):
				print(stock_details)

				# Add the fetched available qty to the total
				row.available_in_store = stock_details[0]['qty']
