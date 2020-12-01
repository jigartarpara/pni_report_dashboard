// Copyright (c) 2016, Jigar Tarpara and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["BOM Explorer Report"] = {
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
	]
};
