# Copyright (c) 2013, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import pandas as pd
from pni_report_dashboard.pni_report_dashboard.report.bom_manufacturing_report.bom_manufacturing_report import get_data, get_stock_balance


def execute(filters=None):
	if not filters: filters = {}
	data = []
	columns = get_columns()
	get_data(filters, data)

	balance = {}
	for raw in data:
		for record in get_bom_stock(filters):
			if not balance.get(raw['item_code']):
				balance[raw['item_code']] = get_stock_balance(raw['item_code'], filters)
			raw['avl_qty'] = balance[raw['item_code']]
			raw['req_qty'] = record[3]
			raw['parts'] = record[5]

	if data:
		df = pd.DataFrame(data)
		df.groupby(['item_code']).sum().reset_index()
		print(list(df.T.to_dict().values()))
		return columns, list(df.T.to_dict().values())

	if get_bom_stock(filters):
		for record in get_bom_stock(filters):
			print(record[3])
		data.append({
			'item_code': record[0],
			'item_name': record[1],
			'bom': '',
			'qty': record[2],
			'avl_qty': 0,
			'description': record[1],
			'scrap': 0,
			'req_qty': record[3],
			'parts': record[4]

		})
	return columns, data

def get_columns():
	"""return columns"""
	columns = [
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
			"label": "Available Qty",
			"fieldtype": "data",
			"fieldname": "avl_qty",
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
		{
			"label": "Required Qty",
			'fieldtype': "data",
			'fieldname': 'req_qty',
			"width": 120
		},
		{
			"label": "Enough Parts to Build",
			'fieldtype': "data",
			'fieldname': 'parts',
			"width": 200
		}
	]


	return columns

def get_bom_stock(filters):
	conditions = ""
	bom = filters.get("bom")

	table = "`tabBOM Item`"
	qty_field = "qty"

	qty_to_produce = filters.get("qty_to_produce", 1)
	if  int(qty_to_produce) <= 0:
		frappe.throw(_("Quantity to Produce can not be less than Zero"))

	if filters.get("show_exploded_view"):
		table = "`tabBOM Explosion Item`"
		qty_field = "stock_qty"

	if filters.get("warehouse"):
		warehouse_details = frappe.db.get_value("Warehouse", filters.get("warehouse"), ["lft", "rgt"], as_dict=1)
		if warehouse_details:
			conditions += " and exists (select name from `tabWarehouse` wh \
				where wh.lft >= %s and wh.rgt <= %s and ledger.warehouse = wh.name)" % (warehouse_details.lft,
				warehouse_details.rgt)
		else:
			conditions += " and ledger.warehouse = %s" % frappe.db.escape(filters.get("warehouse"))

	else:
		conditions += ""

	return frappe.db.sql("""
			SELECT
				bom_item.item_code,
				bom_item.description ,
				bom_item.{qty_field},
				bom_item.{qty_field} * {qty_to_produce} / bom.quantity as req_qty,
				sum(ledger.actual_qty) as actual_qty,
				sum(FLOOR(ledger.actual_qty / (bom_item.{qty_field} * {qty_to_produce} / bom.quantity)))
			FROM
				`tabBOM` AS bom INNER JOIN {table} AS bom_item
					ON bom.name = bom_item.parent
				LEFT JOIN `tabBin` AS ledger
					ON bom_item.item_code = ledger.item_code
				{conditions}
			WHERE
				bom_item.parent = '{bom}' and bom_item.parenttype='BOM'

			GROUP BY bom_item.item_code""".format(
				qty_field=qty_field,
				table=table,
				conditions=conditions,
				bom=bom,
				qty_to_produce=qty_to_produce or 1)
			)