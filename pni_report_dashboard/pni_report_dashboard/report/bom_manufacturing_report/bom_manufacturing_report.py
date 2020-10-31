# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from pprint import pprint
import pandas as pd

def execute(filters=None):
	data = []
	columns = get_columns()
	get_data(filters, data)
	print(data)
	df = pd.DataFrame(data)
	df.groupby(['item_code']).sum().reset_index()
	print(list(df.T.to_dict().values()))
	return columns, list(df.T.to_dict().values())

def get_data(filters, data):
	get_exploded_items(filters.bom,filters.qty_to_produce, data)

def get_exploded_items(bom, qty_to_produce, data, indent=0):
	exploded_items = frappe.get_all("BOM Item",
		filters={"parent": bom, "bom_no": ('!=', '')},
		fields= ['qty','bom_no','qty','scrap','item_code','item_name','description','uom'])

	for item in exploded_items:
		item["indent"] = indent
		data.append({
			'item_code': item.item_code,
			'item_name': item.item_name,
			'indent': indent,
			'bom': item.bom_no,
			'qty': item.qty * qty_to_produce,
			'uom': item.uom,
			'description': item.description,
			'scrap': item.scrap
			})
		if item.bom_no:
			get_exploded_items(item.bom_no, item.qty * qty_to_produce, data, indent=indent+1)

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

