# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from pprint import pprint
import sys

sys.setrecursionlimit(15000)

def execute(filters=None):
	data = []
	columns = get_columns()
	get_data(filters, data)
	return columns, data

def get_data(filters, data):
	try:
		frappe.log_error(message="BOM Explorer Report Started" , title="BOM Explore Report Log 1")
		get_exploded_items(filters.bom, data)
		frappe.log_error(message="BOM Explorer Report Complete" , title="BOM Explore Report Log 2")
	except:
		frappe.log_error(message="BOM Explorer Report Complete 4" , title="BOM Explore Report Log 4")
		title = "Error while processing BOM Explorer Report"
		traceback = frappe.get_traceback()
		frappe.log_error(message=traceback , title=title)
	frappe.log_error(message="BOM Explorer Report Complete 2" , title="BOM Explore Report Log 3")
def get_exploded_items(bom, data, indent=0):
	exploded_items = frappe.db.sql("select qty,bom_no,qty,scrap,item_code,item_name,description,uom from `tabBOM Item` where parent = %s",bom,as_dict=1)
	# exploded_items = frappe.get_all("BOM Item",
	# 	filters={"parent": bom},
	# 	fields= ['qty','bom_no','qty','scrap','item_code','item_name','description','uom'])
	if exploded_items:
		for item in exploded_items:
			item["indent"] = indent
			data.append({
				'item_code': item.item_code,
				'item_name': item.item_name,
				'indent': indent,
				'bom': item.bom_no,
				'qty': item.qty,
				'uom': item.uom,
				'description': item.description,
				'scrap': item.scrap
				})
			if item.bom_no:
				# frappe.db.commit()
				get_exploded_items(item.bom_no, data, indent=indent+1)

def get_columns():
	return [
		{
			"label": "Item Code",
			"fieldtype": "Link",
			"fieldname": "item_code",
			"width": 300,
			"options": "Item"
		},
		{
			"label": "Item Name",
			"fieldtype": "data",
			"fieldname": "item_name",
			"width": 100
		},
		{
			"label": "BOM",
			"fieldtype": "Link",
			"fieldname": "bom",
			"width": 150,
			"options": "BOM"
		},
		{
			"label": "Qty",
			"fieldtype": "data",
			"fieldname": "qty",
			"width": 100
		},
		{
			"label": "UOM",
			"fieldtype": "data",
			"fieldname": "uom",
			"width": 100
		},
		{
			"label": "Standard Description",
			"fieldtype": "data",
			"fieldname": "description",
			"width": 150
		},
		{
			"label": "Scrap",
			"fieldtype": "data",
			"fieldname": "scrap",
			"width": 100
		},
	]
