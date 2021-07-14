# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PriceSchedule(Document):
	pass

@frappe.whitelist()
def address_query(name):
	if name:
		address_lists = frappe.db.get_all("Address",{'name':name},["name","address_line1","address_line2","city","state","country","pincode"])
		if address_lists:
			return address_lists

@frappe.whitelist()
def contact_query(name):
	if name:
		contact_info = {
			'mobile_no' :'',
			'email' :'',
			'first_name':'',
			'middle_name':'',
			'last_name':'' 
		}
		contact_doc = frappe.get_doc("Contact",name)
		if contact_doc:		
			contact_info['first_name'] = contact_doc.get('first_name')
			contact_info['middle_name'] = contact_doc.get('middle_name')
			contact_info['last_name'] = contact_doc.get('last_name')
			for phone in contact_doc.phone_nos:
				if phone.get('is_primary_mobile_no'):
					contact_info['mobile_no'] = phone.get('phone')
			for email in contact_doc.email_ids:
				if email.get('is_primary'):
					contact_info['email'] = email.get('email_id')		
			return contact_info		


@frappe.whitelist()
def fetch_address_contact_name(name):
	if name:
		address_contact_name = {
			'address_name' :'',
			'contact_name' :'' 
		}
		add_name = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Customer', 'link_name': name, 'parenttype': 'Address'}, fields=['parent'])
		con_name = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Customer', 'link_name': name, 'parenttype': 'Contact'}, fields=['parent'])
		address_contact_name['address_name'] = add_name[0].get('parent')
		address_contact_name['contact_name'] = con_name[0].get('parent')
		if add_name and con_name:
			return address_contact_name


@frappe.whitelist()
def number_to_word(amount):
	def get_word(n):
		words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
		if n<=20:
			return words[n]
		else:
			ones=n%10
			tens=n-ones
			return words[tens]+" "+words[ones]

	def get_all_word(n):
		d=[100,10,100,100]
		v=["","Hundred And","Thousand","lakh"]
		w=[]
		for i,x in zip(d,v):
			t=get_word(n%i)
			if t!="":
				t+=" "+x
			w.append(t.rstrip(" "))
			n=n//i
		w.reverse()
		w=' '.join(w).strip()
		if w.endswith("And"):
			w=w[:-3]
		return w

	arr=str(amount).split(".")
	amount=int(arr[0])
	crore=amount//10000000
	amount=amount%10000000
	word=""
	if crore>0:
		word+=get_all_word(crore)
		word+=" crore "
	word+=get_all_word(amount).strip()+" only."
	if len(arr)>1:
		if len(arr[1])==1:
			arr[1]+="0"
		word+=" and "+get_all_word(int(arr[1]))+" paisa"
	
	return word


@frappe.whitelist()
def calculate_taxes(tax_temlet_name,total_amount):
	try:
		tax_items = []
		tx_calculation = 0.0
		total_tax_amount =0.0
		tax_details = frappe.get_doc("Sales Taxes and Charges Template", tax_temlet_name).taxes
		for taxes in tax_details:
			tx_calculation = int(total_amount)/100*taxes.rate
			if taxes.idx == 1:
				total_tax_amount =int(total_amount) + tx_calculation
			else:
				total_tax_amount = total_tax_amount + tx_calculation

			temp = {
				'charge_type' : taxes.charge_type,
				'account_head' : taxes.account_head,
				'description' : taxes.description,
				'rate' : taxes.rate,
				'tax_amount' : tx_calculation,
				'total':total_tax_amount
			}
			tax_items.append(temp)
		return tax_items
	except Exception as e:
		raise e


