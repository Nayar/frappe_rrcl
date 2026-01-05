import frappe

@frappe.whitelist(allow_guest=True)
def postevent():
    return {"status": "ok", "message": "ok"}