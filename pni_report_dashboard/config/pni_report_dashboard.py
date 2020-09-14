from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Engineering"),
			"items": [
				{
					"type": "report",
					"name": "Item Price List Report",
					"description": _("Item Price List Report"),
					"is_query_report": True,
					"reference_doctype": "Item Price",
				}
			]
		}
	]