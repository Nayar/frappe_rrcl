// Copyright (c) 2026, LEFINTECH LTD and contributors
// For license information, please see license.txt

// frappe.ui.form.on("RRCL Employee Overtime", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('RRCL Employee Overtime Item', { // Replace with your actual child table DocType name
    table_wiyb_add: function(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (frm.doc.default_overtime_start) {
            frappe.model.set_value(cdt, cdn, 'overtime_start', frm.doc.default_overtime_start);
        }
        if (frm.doc.default_overtime_end) {
            frappe.model.set_value(cdt, cdn, 'overtime_end', frm.doc.default_overtime_end);
        }
        if (frm.doc.default_overtime_hrs) {
            frappe.model.set_value(cdt, cdn, 'overtime_hrs', frm.doc.default_overtime_hrs);
        }
    }
});