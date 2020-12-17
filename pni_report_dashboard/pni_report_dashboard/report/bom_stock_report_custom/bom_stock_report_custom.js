// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BOM Stock Report Custom"] = {
	"filters": [
		{
			fieldname: "bom",
			label: __("BOM"),
			fieldtype: "Link",
			options: "BOM",
			reqd: 1,
			get_query: function(){
				return {
					'filters': [['BOM', 'is_default', '=', '1']]
				}
			} 
		},
		{
			fieldname: "qty_to_produce",
			label: __("Quantity to Produce"),
			fieldtype: "Int",
			default: "1",
			reqd: 1
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse"
		}
	]
};
