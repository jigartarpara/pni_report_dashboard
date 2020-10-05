# -*- coding: utf-8 -*-
# Copyright (c) 2020, Jigar Tarpara and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DailyPCCosting(Document):
	def get_brand_list(self):
		if self.brand_group:
			doc = frappe.get_doc("Brand Group", self.brand_group)
			if doc:
				return doc.brand_group_table
	
	def validate(self):
		self.calculate_data()

	def calculate_data(self):
		for raw in self.dail_pc_costing:
			self.get_total_production(raw)
	
	def get_total_production(self, raw):
		brand = raw.brand
		data = frappe.db.sql(""" 
			select sum(sed.qty),sum(pni_packing.total_net_weight)
				from 
					`tabStock Entry Detail` as sed,
					`tabStock Entry` as se,
					`tabItem` as item,
					`tabPNI Packing` as pni_packing
				where se.name = sed.parent
					and se.posting_date = '{date}'
					and sed.item_code = item.name
					and item.brand = '{brand}'
					and pni_packing.name = se.pni_reference
					and se.pni_reference_type = 'PNI Packing'
		""".format(date=self.date,brand=brand))

		if len(data) and len(data[0]):
			raw.total_cup_production = data[0][0]
			raw.net_weight = data[0][1]
		
		# f1 = (net weight + blank Scarp) * blank rate
		raw.f1 = ( raw.net_weight + raw.blank_scrap ) * raw.blank_rate

		# f2 = bottom scrap * bottom rate
		raw.f2 = raw.bottom_scrap * raw.bottom_rate

		# f3 = (f1+f2) / total_cup_production
		raw.f3 = (raw.f1+raw.f2)/ raw.total_cup_production
		