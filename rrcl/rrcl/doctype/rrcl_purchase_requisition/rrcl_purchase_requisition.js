frappe.ui.form.on("RRCL Purchase Requisition", {
  scan_barcode: function(frm) {
    const barcode = frm.doc.scan_barcode;
    if (!barcode) {
      return;
    }

    frappe.call({
      method: "frappe.client.get",
      args: {
        doctype: "RRCL Item",
        filters: { rrcl_name: barcode },
        fieldname: ["name", "item_code", "item_name"]
      },
      callback: function(response) {
        const item = response.message;
        if (!item) {
          frappe.msgprint(__('Item not found for the scanned barcode.'));
          return;
        }

        // Add a new child row
        const row = frm.add_child("table_vqjn", {
          item: item.name
          // … other fields …
        });

        // Refresh the table field so the new row shows
        frm.refresh_field("table_vqjn");

        // Use a delay to ensure grid is rendered before opening
        setTimeout(() => {
          frm.get_field("table_vqjn").grid.open_grid_row(row.name);
        }, 100);  // 100 ms delay

        // Or, more “Frappe-idiomatic”: open after AJAX
        frappe.after_ajax(() => {
            const grid = frm.get_field("table_vqjn").grid;
            const idx = frm.doc.table_vqjn.findIndex(r => r.name === row.name);

            if (idx !== -1 && grid.grid_rows[idx]) {
                grid.grid_rows[idx].toggle_view();   // This works in Frappe 15
            }
        });

        // Clear barcode input
        frm.set_value('scan_barcode', '');
      },
      error: function(err) {
        frappe.msgprint(__('Error fetching item details.'));
      }
    });
  }
});
