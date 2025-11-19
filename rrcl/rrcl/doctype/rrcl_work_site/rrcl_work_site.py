# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RRCLWorkSite(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        amended_from: DF.Link | None
        site_name: DF.SmallText
        warehouse: DF.Link | None
    # end: auto-generated types

    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.
    
    from typing import TYPE_CHECKING
    
    if TYPE_CHECKING:
      from frappe.types import DF
      
      amended_from: DF.Link | None
      site_name: DF.SmallText
	# end: auto-generated types

    def on_update(self):
        return
        if not self.warehouse:
            warehouse_name = f"{self.site_name} - Store"
            existing_warehouse = frappe.db.get_value("Warehouse", {"warehouse_name": warehouse_name})

            if not existing_warehouse:
                warehouse = frappe.get_doc({
                    "doctype": "Warehouse",
                    "warehouse_name": warehouse_name,
                    "company": getattr(self, "company", frappe.defaults.get_defaults().get("company")),
                    "is_group": 0
                })
                warehouse.insert(ignore_permissions=True)
                frappe.msgprint(f"Warehouse '{warehouse.name}' created for this Work Site.")
            else:
                warehouse = frappe.get_doc(existing_warehouse)
            self.db_set("warehouse", warehouse.name)

        