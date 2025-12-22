# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from datetime import datetime


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

	def before_submit(self):
		self.validate_allowed_day()

	def validate_allowed_day(self):
		# Fetch setting
		allowed_day = frappe.db.get_single_value(
			"RRCL Settings",
			"allow_pr_on_date"
		)

		# If not set or set to All, allow submission
		if not allowed_day or allowed_day == "All":
			return

		# Get today's weekday (e.g. Monday)
		today = datetime.today().strftime("%A")

		if today != allowed_day:
			frappe.throw(
				f"Purchase Requisition submission is only allowed on **{allowed_day}**. "
				f"Today is **{today}**."
			)
