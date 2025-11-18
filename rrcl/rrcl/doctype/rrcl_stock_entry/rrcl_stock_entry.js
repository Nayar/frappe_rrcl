frappe.ui.form.on('RRCL Stock Entry', {
    setup(frm){
        frm.set_query('rrcl_pr', () => {
            return {
                filters: {
                    docstatus: 1,
                    workflow_state: ["!=", "Completed"]
                }
            }
        })
    },
    rrcl_pr(frm) {
        // Make sure rrcl_pr has a value
        if (!frm.doc.rrcl_pr) {
            frm.clear_table('table_nerq');
            frm.refresh_field('table_nerq');
            return;
        }
        
        // Fetch the linked Purchase Requisition
        frappe.db.get_doc('RRCL Purchase Requisition', frm.doc.rrcl_pr)
            .then(pr_doc => {
                // Check that work_site exists
                if (pr_doc.work_site) {
                    frm.set_value('work_site', pr_doc.work_site);
                    //frm.set_df_property('work_site', 'read_only', 1);
                    frm.refresh_field('work_site');
                    
                }

                // Clear and refill target child table
                frm.clear_table('table_nerq');

                // Confirm the source table exists
                if (pr_doc.table_vqjn && pr_doc.table_vqjn.length > 0) {
                    pr_doc.table_vqjn.forEach(row => {
                        let child = frm.add_child('table_nerq');
                        child.item = row.item;
                        child.qty = row.qty;
                    });
                } else {
                    frappe.msgprint(__('No items found in the selected Purchase Requisition.'));
                }
                //frm.refresh_field('table_nerq',"RRCL Item","item");
                frm.refresh_field('table_nerq');
                frm.save()
                frm.refresh()
                //frm.fields_dict.table_nerq.grid.refresh();
                // Refresh to show data
                
            })
            .catch(err => {
                frappe.msgprint(__('Failed to fetch Purchase Requisition: ' + err));
            });
    }
});
