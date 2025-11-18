# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class RRCLItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		allow_in_purchase_requisition: DF.Check
		barcode: DF.Barcode | None
		image: DF.AttachImage | None
		rrcl_name: DF.Data
		standard_name: DF.Data | None
	# end: auto-generated types

	pass
