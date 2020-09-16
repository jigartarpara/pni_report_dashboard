import frappe
@frappe.whitelist()
def get_carton():
	sql  = frappe.db.sql("""
		select sum(qty)  
			from `tabStock Entry Detail`
		where docstatus=1 and item_group="paper reel"
	""")
	data = 0
	if sql[0] and sql[0][0]:
		data = sql[0][0]
	return data

@frappe.whitelist()
def get_ldpe():
	sql  = frappe.db.sql("""
		select sum(qty)  
			from `tabStock Entry Detail`
		where docstatus=1 and item_code="LDP LA 17"
	""")
	data = 0
	if sql[0] and sql[0][0]:
		data = sql[0][0]
	return data