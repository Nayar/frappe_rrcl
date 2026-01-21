// Copyright (c) 2026, LEFINTECH LTD and contributors
// For license information, please see license.txt

// frappe.ui.form.on("RRCL HIK Vision Attendance Upload", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('RRCL HIK Vision Attendance Upload', {
    refresh: function(frm) {
        if (frm.doc.attach_mvjs) {
            frm.add_custom_button(__('Process CSV'), function() {
                frm.call('process_csv');
            });
        }
    }
});