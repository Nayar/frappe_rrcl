// Copyright (c) 2026, LEFINTECH LTD and contributors
// For license information, please see license.txt

// frappe.ui.form.on("RRCL Timesheet", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('RRCL Timesheet', {
    refresh: function(frm) {
        frm.add_custom_button(__('Generate Present from Devices'), function() {
            frm.call('generate_present');
        });
    }
});