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
		blank_scrap_query = frappe.db.sql("""
			select  se.name, sed.item_code, sum(sed.qty), se.pni_reference
				from 
					`tabStock Entry Detail` as sed,
					`tabStock Entry` as se
				where se.docstatus=1 and se.name = sed.parent
					and se.posting_date = '{date}'
					and se.scrap_entry = 1
					and se.pni_reference_type = "Workstation"
					and sed.item_code = 'Blank Paper Scrap'
				group by sed.item_code
		""".format(date=self.date_for_costing))
		print(blank_scrap_query)

		bottom_scrap_query = frappe.db.sql("""
			select  se.name, sed.item_code, sum(sed.qty), se.pni_reference
				from 
					`tabStock Entry Detail` as sed,
					`tabStock Entry` as se
				where se.docstatus=1 and se.name = sed.parent
					and se.posting_date = '{date}'
					and se.scrap_entry = 1
					and se.pni_reference_type = "Workstation"
					and sed.item_code = 'Bottom Paper Scrap'
				group by sed.item_code
		""".format(date=self.date_for_costing))
		print(bottom_scrap_query)

		data = frappe.db.sql(""" 
			select sum(pni_packing.total_stock), pni_packing.name
				from
					`tabPNI Packing` as pni_packing
				where 
					pni_packing.docstatus = 1
					and pni_packing.date = '{date}'
		""".format(date=self.date_for_costing))
		print(data)

		total_blank_scrap = sum([entry[2] for entry in blank_scrap_query])
		# print(total_blank_scrap)
		total_bottom_scrap = sum([entry[2] for entry in bottom_scrap_query])
		# print(total_bottom_scrap)
		total_cup_production = sum([int(entry[0]) for entry in data])
		# print(total_cup_production)

		blank_scrap_ratio = total_blank_scrap / total_cup_production
		bottom_scrap_ratio = total_bottom_scrap / total_cup_production
		print(blank_scrap_ratio)
		print(bottom_scrap_ratio)


		for raw in self.dail_pc_costing:
			self.get_total_production(raw)
			raw.blank_scrap = raw.total_cup_production * blank_scrap_ratio
			raw.bottom_scrap = raw.total_cup_production * bottom_scrap_ratio
			print(raw.blank_scrap)
			print(raw.bottom_scrap)

			
			# self.calculate_blank_scrap(raw)
			# self.calculate_bottom_scrap(raw)
	
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
		""".format(date=self.date_for_costing,brand=brand))

		if len(data) and len(data[0]):
			raw.total_cup_production = data[0][0]
			raw.net_weight = data[0][1]
		

		# self.calculate_blank_scrap(raw)
		# self.calculate_bottom_scrap(raw)
		
		
		if not raw.net_weight:
			raw.net_weight = 0
		if not raw.blank_scrap:
			raw.blank_scrap = 0
		if not raw.blank_rate:
			raw.blank_rate = 0
		if not raw.bottom_scrap:
			raw.bottom_scrap = 0
		if not raw.bottom_rate:
			raw.bottom_rate  = 0
		if not raw.total_cup_production:
			raw.total_cup_production = 0
		
		# f1 = (net weight + blank Scarp) * blank rate
		raw.f1 = ( float(raw.net_weight) + float(raw.blank_scrap) ) * float(raw.blank_rate)

		# f2 = bottom scrap * bottom rate
		raw.f2 = float(raw.bottom_scrap) * float(raw.bottom_rate)

		# f3 = (f1+f2) / total_cup_production
		if raw.total_cup_production > 0 :
			raw.f3 = (float(raw.f1)+float(raw.f2))/ float(raw.total_cup_production)
		else:
			raw.f3 = 0
	
	# def calculate_blank_scrap(self, raw):
	# 	blank_scrap_query = frappe.db.sql(""" 
	# 		select se.name, sed.item_code, sed.qty, se.pni_reference, pni_packing.total_stock, pni_packing.item
	# 			from 
	# 				`tabStock Entry Detail` as sed,
	# 				`tabStock Entry` as se,
	# 				`tabItem` as item,
	# 				`tabPNI Packing` as pni_packing
	# 			where se.name = sed.parent
	# 				and se.posting_date = '{date}'
	# 				and sed.item_code = item.name
	# 				and se.scrap_entry = 1
	# 				and se.pni_reference_type = "Workstation"
	# 				and se.pni_reference = pni_packing.workstation
	# 				and sed.item_code = 'Blank Paper Scrap'
	# 			group by se.name
	# 	""".format(date=self.date_for_costing))

	# 	self.items_stock_query = frappe.db.sql("""
	# 		select pni_packing.total_stock, pni_packing.item, pni_packing.workstation
	# 			from 
	# 				`tabStock Entry Detail` as sed,
	# 				`tabStock Entry` as se,
	# 				`tabItem` as item,
	# 				`tabPNI Packing` as pni_packing
	# 			where pni_packing.docstatus = 1 and se.name = sed.parent
	# 				and se.posting_date = '{date}'
	# 				and sed.item_code = item.name
	# 				and se.pni_reference_type = "Workstation"
    #                 and se.pni_reference = pni_packing.workstation
	# 			group by 
	# 				pni_packing.name
	# 	""".format(date=self.date_for_costing))

	# 	print("in blank scrap")
	# 	#For Total blank scrap
	# 	total_blank_scrap = 0
	# 	total_cup_stock = 0
	# 	total_blank_scrap = sum([entry[2] for entry in blank_scrap_query])
	# 	print(total_blank_scrap)

	# 	#For items stock query
	# 	total_cup_stock = sum([int(entry[0]) for entry in self.items_stock_query])
	# 	print(total_cup_stock)

	# 	for entry in self.items_stock_query:
	# 		scrap_ratio = (int(entry[0])/total_cup_stock) * total_blank_scrap
	# 		print(scrap_ratio)
	# 	pass

	# 	# for scrap in blank_scrap_ratio:
	# 	# 	raw.blank_scrap = sum(scrap)
	
	# def calculate_bottom_scrap(self, raw):
	# 	bottom_scrap_query = frappe.db.sql(""" 
	# 		select se.name, sed.item_code, sed.qty, se.pni_reference, pni_packing.total_stock, pni_packing.item
	# 			from 
	# 				`tabStock Entry Detail` as sed,
	# 				`tabStock Entry` as se,
	# 				`tabItem` as item,
	# 				`tabPNI Packing` as pni_packing
	# 			where se.name = sed.parent
	# 				and se.posting_date = '{date}'
	# 				and sed.item_code = item.name
	# 				and se.scrap_entry = 1
	# 				and se.pni_reference_type = "Workstation"
	# 				and se.pni_reference = pni_packing.workstation
	# 				and sed.item_code = 'Bottom Paper Scrap'
	# 			group by se.name
	# 	""".format(date=self.date_for_costing))

	# 	#For Total bottom scrap
	# 	total_bottom_scrap = 0
	# 	total_cup_stock = 0
	# 	total_bottom_scrap = sum([entry[2] for entry in bottom_scrap_query])
	# 	print(total_bottom_scrap)

	# 	#For items stock query
	# 	total_cup_stock = sum([int(entry[0]) for entry in self.items_stock_query])
	# 	print(total_cup_stock)

	# 	for entry in self.items_stock_query:
	# 		scrap_ratio = (int(entry[0])/total_cup_stock) * total_bottom_scrap
	# 		print(scrap_ratio)
	# 	pass