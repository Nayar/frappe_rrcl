# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RRCLStockEntry(Document):
  # begin: auto-generated types
  # This code is auto-generated. Do not modify anything in this block.
  
  from typing import TYPE_CHECKING
  
  if TYPE_CHECKING:
    from erpnext.rrcl.doctype.rrcl_stock_entry_item.rrcl_stock_entry_item import RRCLStockEntryItem
    from frappe.types import DF
    
    amended_from: DF.Link | None
    date: DF.Date | None
    rrcl_pr: DF.Link | None
    table_nerq: DF.Table[RRCLStockEntryItem]
    work_site: DF.Link
    # end: auto-generated types
  
  pass

  def on_submit(self):
    print(self.rrcl_pr)
    pr = frappe.get_doc("RRCL Purchase Requisition", self.rrcl_pr)
    for row_se in self.table_nerq:
      print("loop 1")
      for row_pr in pr.table_vqjn:
        print("loop 2")
        if(row_pr.item == row_se.item):
          pr_item = frappe.get_doc("RRCL Purchase Requisition Item",row_pr.name)
          total_delivered = (pr_item.delivered or 0) + row_se.qty
          pr_item.db_set("delivered", total_delivered)
          pr_item.db_set("fulfilled", pr_item.qty <= total_delivered)
          frappe.get_doc("RRCL Purchase Requisition", pr_item.parent).add_comment(
              "Info",
              f"Delivered qty for item {row_se.item} updated to {total_delivered}"
              f"by Stock Entry {self.name}."
          )
          # pr_item.delivered = (pr_item.delivered or 0) + row_se.qty
          # pr_item.save()
          # print("match")
    return False
          

  
