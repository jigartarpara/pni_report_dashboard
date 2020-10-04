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
