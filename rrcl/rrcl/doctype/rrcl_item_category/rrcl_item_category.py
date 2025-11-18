# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils.nestedset import NestedSet


class RRCLItemCategory(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		is_group: DF.Check
		lft: DF.Int
		name1: DF.Data | None
		parent_rrcl_item_category: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types

	pass
