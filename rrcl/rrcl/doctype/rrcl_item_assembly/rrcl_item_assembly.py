import frappe
from frappe.model.document import Document

class RRCLItemAssembly(Document):
    def validate(self):
        """Automatically runs when the document is saved."""
        self.calculate_formulas()

    def calculate_formulas(self):
        # 1. Setup the execution context
        # We use a default of 1.0 for quantity to avoid division by zero errors
        context = {
            "input1": self.quantity if getattr(self, "quantity", None) else 1.0, 
            "result": 0.0
        }

        # 2. Map the child table rows to variables
        # Using field name 'table_eccy' from your screenshot
        for row in self.table_eccy:
            if row.variable:
                # Allows formulas to use excavator_rental.rate, etc.
                context[row.variable] = row

        # 3. Execution helper
        def run_logic(code_str):
            if not code_str:
                return 0.0
            
            local_scope = context.copy()
            try:
                # Execute the string code from the 'Code' type fields
                exec(str(code_str), {}, local_scope)
                return float(local_scope.get("result", 0.0))
            except Exception as e:
                frappe.msgprint(f"Error in formula execution: {str(e)}")
                return 0.0

        # 4. Update the target fields using names from your screenshot
        self.unit_price = run_logic(self.variable_cost_formula)
        self.fixed_cost = run_logic(self.fixed_cost_formula)
        self.estimated_duration = run_logic(self.estimated_duration_formula)

        self.fixed_cost_for_input = self.fixed_cost
        self.variable_cost_for_input = self.input1 * self.unit_price
        self.estimated_duration_for_input = self.input1 * self.estimated_duration