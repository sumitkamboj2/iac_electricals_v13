# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def before_insert(self,method=None):
	self.flags.name_set = 1

	current = frappe.db.sql("""select MAX(current) AS current from `tabSeries` where name = '{0}'""".format(self.custom_naming_series),as_dict=1)
	for row in current:
		current = row.current

	if current is None:
		current = 1
		series = self.custom_naming_series + str(current).zfill(3)
		self.name = series
		first_series_to_store = self.custom_naming_series 
		frappe.db.sql("insert into tabSeries (name, current) values (%s, 1)", (first_series_to_store))
	else:
		current = current + 1
		current = current
		series = self.custom_naming_series + str(current).zfill(3)
		self.name = series
		frappe.db.sql("""update tabSeries set current = {0} where name = '{1}'""".format(current, self.custom_naming_series))


@frappe.whitelist()
def update_old_item_custom_naming_series_for_one_time():
	all_item = frappe.get_all('Item')
	cnt = 0
	for item in all_item:
		cnt = cnt + 1
		sql = """ UPDATE `tabItem` SET custom_naming_series = "" where name IN ('{0}')""".format(item.name)
		benificiary_purchase_count = frappe.db.sql(sql,debug=1)

	error_log = frappe.log_error(frappe.get_traceback(), _("All item Updated item count: '{0}' ").format(cnt))		


@frappe.whitelist()
def update_the_series_item_updation(prefix_level_for_item,count1):
	item_updation = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count1, prefix_level_for_item), debug = 1)
	return "Success"


@frappe.whitelist()
def update_the_series_prefix2_updation(prefix_level_3, count2):
	item_updation = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count2, prefix_level_3), debug = 1)
	return "Success"


@frappe.whitelist()
def update_the_series_prefix3_updation(prefix_level_2, count3):
	item_updation = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count3, prefix_level_2), debug = 1)
	return "Success"