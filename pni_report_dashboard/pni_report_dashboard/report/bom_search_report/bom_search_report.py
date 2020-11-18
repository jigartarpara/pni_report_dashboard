# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json

from six import iteritems

def execute(filters=None):
	data = []
	parents = {
		"Product Bundle Item": "Product Bundle",
		"BOM Explosion Item": "BOM",
		"BOM Item": "BOM"
	}

	for doctype in ("Product Bundle Item",
		"BOM Explosion Item" if filters.search_sub_assemblies else "BOM Item"):
		for d in frappe.get_all(doctype, fields=["parent", "item_code", "name"]):
			valid = True
			for key, item in iteritems(filters):
				if key != "search_sub_assemblies":
					if item and item != d.item_code:
						valid = False

			if valid:
				data.append((d.parent, parents[doctype], d.name))

	return [{
		"fieldname": "parent",
		"label": "BOM",
		"width": 200,
		"fieldtype": "Dynamic Link",
		"options": "doctype"
	},
	{
		"fieldname": "doctype",
		"label": "Type",
		"width": 200,
		"fieldtype": "Data"
	},
	{
		"fieldname": "bom_item",
		"label": "BOM Item",
		"width": 200,
		"fieldtype": "Link",
		"options": "BOM Item"
	}], data

