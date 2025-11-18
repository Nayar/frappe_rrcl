# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class RRCLPurchaseRequisition(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from erpnext.rrcl.doctype.rrcl_purchase_requisition_item.rrcl_purchase_requisition_item import RRCLPurchaseRequisitionItem
		from frappe.types import DF

		amended_from: DF.Link | None
		approved_by: DF.Link | None
		date: DF.Date | None
		generated_by: DF.Link | None
		table_vqjn: DF.Table[RRCLPurchaseRequisitionItem]
		work_site: DF.Link
		workflow_state: DF.Data | None
	# end: auto-generated types

	pass
