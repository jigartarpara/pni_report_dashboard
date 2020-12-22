// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BOM Stock and Manufacturing Report"] = {
	"filters": [
		{
			"fieldname": "bom",
			"label": __("BOM"),
			"fieldtype": "Link",
			"options": "BOM",
			"reqd": 1,
			get_query: function(){
				return {
					'filters': [['BOM', 'is_default', '=', '1']]
				}
			} 
		}, {
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"reqd": 1
		}, {
			"fieldname": "show_exploded_view",
			"label": __("Show exploded view"),
			"fieldtype": "Check"
		}, {
			"fieldname": "qty_to_produce",
			"label": __("Quantity to Produce"),
			"fieldtype": "Int",
			"default": "1"
		 },
	],
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column.id == "Item"){
			if (data["Enough Parts to Build"] > 0){
				value = `<a style='color:green' href="#Form/Item/${data['Item']}" data-doctype="Item">${data['Item']}</a>`
			} else {
				value = `<a style='color:red' href="#Form/Item/${data['Item']}" data-doctype="Item">${data['Item']}</a>`
			}
		}
		return value
	}
};
