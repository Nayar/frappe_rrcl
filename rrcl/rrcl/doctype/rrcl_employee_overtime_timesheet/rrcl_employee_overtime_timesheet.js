// Copyright (c) 2026, LEFINTECH LTD and contributors
// For license information, please see license.txt

// frappe.ui.form.on("RRCL Employee Overtime Timesheet", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('RRCL Employee Overtime Timesheet', {
    update_times: function(frm) {
        update_child_table_times(frm, 'overtime_start', frm.doc.default_overtime_start);
        update_child_table_times(frm, 'overtime_end',   frm.doc.default_overtime_end);
        update_child_table_times(frm, 'overtime_hrs',   frm.doc.default_overtime_hrs);
    }
});

frappe.ui.form.on('RRCL Employee Overtime Timesheet Details', { // Replace with your actual child table DocType name
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

function update_child_table_times(frm, field_name, value) {
    if (frm.doc.table_wiyb && value) { // Replace 'employees' with your actual table fieldname
        frm.doc.table_wiyb.forEach(row => {
            frappe.model.set_value(row.doctype, row.name, field_name, value);
        });
        frm.refresh_field('employees');
    }
}