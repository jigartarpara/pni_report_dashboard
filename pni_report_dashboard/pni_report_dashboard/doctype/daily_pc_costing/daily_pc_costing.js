// Copyright (c) 2020, Jigar Tarpara and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily PC Costing', {
	refresh: function(frm) {
		if(!frm.doc.brand_group){
			frm.doc.dail_pc_costing = ""
			refresh_field("dail_pc_costing");
		}

	},
	brand_group: function(frm) {
		if(!frm.doc.brand_group){
			frm.doc.dail_pc_costing = ""
			refresh_field("dail_pc_costing");
			return
		}
		frappe.call({
			"method": "get_brand_list",
			doc: cur_frm.doc,
			callback: function (r) {
				if(r.message){
					frm.doc.dail_pc_costing = ""
					r.message.forEach(function(element) {
						var c = frm.add_child("dail_pc_costing");
						c.brand = element.brand;
					});
					refresh_field("dail_pc_costing");
				}	
			}
		})
	}
});
