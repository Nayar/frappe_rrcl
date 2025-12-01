import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def receive_procore_webhook():
    """
    Receives Procore webhook payload and creates/updates Frappe records.
    """
    import json

    # Get raw payload
    try:
        payload = frappe.local.form_dict
        # If Procore sends JSON body
        if "payload" in payload:
            data = json.loads(payload.get("payload"))
        else:
            data = json.loads(frappe.local.request.get_data(as_text=True))
        new_doc = frappe.get_doc({
            "doctype": "RRCL WebHook Receiver",
            "body" : data
        })
        new_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        # Optional: verify secret key
        secret_key = frappe.conf.get("procore_webhook_secret")
        if payload.get("token") != secret_key:
            frappe.throw(_("Unauthorized"), frappe.PermissionError)

    except Exception as e:
        frappe.log_error(message=str(e), title="Procore Webhook Error")
        new_doc = frappe.get_doc({
            "doctype": "RRCL WebHook Receiver",
            "body" : {"status": "error", "message": str(e)}
        })
        new_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "error", "message": str(e)}
        
