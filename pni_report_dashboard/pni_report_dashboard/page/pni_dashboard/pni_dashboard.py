import frappe
from frappe.utils import date_diff, add_months, today, getdate, add_days

@frappe.whitelist()
def get_carton():
	_date = add_days(today(), -1)
	sql  = frappe.db.sql("""
		select sum(qty)  
			from `tabStock Entry Detail`
		where docstatus=1 and item_group="paper reel" and posting_date="{0}"
	""".format(_date))
	data = 0
	if sql[0] and sql[0][0]:
		data = sql[0][0]
	return data

@frappe.whitelist()
def get_ldpe():
	_date = add_days(today(), -1)
	sql  = frappe.db.sql("""
		select sum(qty)  
			from `tabStock Entry Detail`
		where docstatus=1 and item_code="LDP LA 17"
		and posting_date="{0}"
	""".format(_date))
	data = 0
	if sql[0] and sql[0][0]:
		data = sql[0][0]
	return data