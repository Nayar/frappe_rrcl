# Copyright (c) 2025, LEFINTECH LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RRCLScaffoldingRequest(Document):
	def before_save(self):
		self.rental_per_day = 0
		# Iterate through the child table rows (table_yngh)
		for row in self.table_yngh:
			print(row.item)
			try:
				self.rental_per_day += float(row.qty * float(frappe.get_doc("RRCL Item",row.item).rental_price))
			except:
				pass
			stock_details = frappe.get_all(
				'RRCL Stock', 
				filters={'item': row.item}, 
				fields=['qty']
			)
			if(len(stock_details)):
				print(stock_details)

				# Add the fetched available qty to the total
				row.available_in_store = stock_details[0]['qty']
			
