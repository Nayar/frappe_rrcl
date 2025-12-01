import frappe
from frappe import _
import json

import requests

class ProcoreAPI:

    COMPANY_ID = "598134325766849"      # you may keep fixed OR pass via settings
    BASE_URL = f"https://api.procore.com/rest/v1.3"
    

    @staticmethod
    def _get_token():
        """Fetch Procore token from RRCL Settings"""
        settings = frappe.get_single("RRCL Settings")   # Gets single doctype entry
        if not settings.procore_token:
            frappe.throw("❗ Procore Token missing in RRCL Settings")
        return settings.get_password("procore_token")

    @staticmethod
    def _headers():
        return {
            "Authorization": f"Bearer {ProcoreAPI._get_token()}",
            "Content-Type": "application/json",
            "Procore-Company-Id": ProcoreAPI.COMPANY_ID
        }

    # -----------------------------------------------------------
    #  STATIC → Get User by Employee ID
    # -----------------------------------------------------------
    @staticmethod
    def get_user_by_employee_id(employee_id):
        url = f"{ProcoreAPI.BASE_URL}/companies/{ProcoreAPI.COMPANY_ID}/users"
        params = {"employee_id": employee_id}
        print(ProcoreAPI._headers())
        response = requests.get(url, headers=ProcoreAPI._headers(), params=params)

        if response.status_code == 200:
            users = response.json()
            return users[0] if users else None
        else:
            frappe.throw(f"❗ Failed fetching Procore User: {response.status_code} {response.text}")

    # -----------------------------------------------------------
    #  STATIC → Create/Update a User in Procore
    # -----------------------------------------------------------
    @staticmethod
    def update_user(doc, run_validations=False):
        """
        user: dict containing:
        first_name, last_name, job_title, is_active, is_employee, employee_id, email_address
        """
        url = f"{ProcoreAPI.BASE_URL}/companies/{ProcoreAPI.COMPANY_ID}/users/{doc['procore_id']}"
        print(url)
        # return {}
        params = {"run_configurable_validations": str(run_validations).lower()}
        payload = {"user": {
            'first_name' : doc['first_name'],
            'last_name' : doc['last_name'],
            'employee_id' : doc['employee_code']
        },"json": True}

        response = requests.put(url, headers=ProcoreAPI._headers(), json=payload, params=params)

        if response.status_code in [200, 201]:
            return response.json()
        else:
            frappe.throw(f"❗ Failed to create/update Procore user: {response.status_code} {response.text}")

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
            "doctype": "RRCL WebHook Event",
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
            "doctype": "RRCL WebHook Event",
            "body" : {"status": "error", "message": str(e)}
        })
        new_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        return {"status": "error", "message": str(e)}
        
@frappe.whitelist()
def sync_employees_to_procore(*args,**kwargs):
    print(kwargs)
    doc = json.loads(kwargs['doc'])

    success_count = 0
    errors = []
    procore_user = ProcoreAPI.update_user(doc)
    return f"Success: {success_count}, Errors: {len(errors)}"