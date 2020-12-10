# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "pni_packing",
			"label": "PNI Packing",
			"fieldtype": "Link",
			"options": "PNI Packing"
		},
		{
			"fieldname": "item_code",
			"label": "Item Code",
			"fieldtype": "Link",
			"options": "Item"
		},
		{
			"fieldname": "workstation",
			"label": "Workstation",
			"fieldtype": "Link",
			"options": "Workstation"
		},
		{
			"fieldname": "source_warehouse",
			"label": "Source Warehouse",
			"fieldtype": "Link",
			"options": "Warehouse"
		},
		{
			"fieldname": "pni_carton",
			"label": "PNI Carton",
			"fieldtype": "Link",
			"options": "PNI Carton"
		},
		{
			"fieldname": "supervisor",
			"label": "Supervisor",
			"fieldtype": "Link",
			"options": "Employee"
		},
		{
			"fieldname": "net_weight",
			"label": "Net Weight",
			"fieldtype": "Float"
		}
	]

def get_data(filters):
	condition = ""
	
	if filters.get("item"):
		condition += " and packing.item = '{0}' ".format(filters.get("item")) 
	
	data = frappe.db.sql("""
		select 
			packing.name,
			packing.item,
			packing.workstation,
			packing.source_warehouse,
			carton.name,
			carton.supervisor,
			carton.net_weight
		from
			`tabPNI Packing` as packing,
			`tabPNI Packing Carton` as packing_carton,
			`tabPNI Carton` as carton
		where
			packing.name = packing_carton.parent
			and packing_carton.carton_id = carton.name
			{0}
	""".format(condition))
	return data