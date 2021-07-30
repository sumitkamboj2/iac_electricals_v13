frappe.ui.form.on("Lead", {
	refresh: function(frm) {
		$("[data-doctype='Quotation']").hide();
	},
})


cur_frm.cscript.custom_refresh= function(frm){
	$('.inner-group-button').find("[data-label='Quotation']").hide();
	/*cur_frm.page.remove_inner_button(__('Quotation'),  __('Create'));*/

	if(cur_frm.doc.status == 'Lead' || cur_frm.doc.status == 'Open' || cur_frm.doc.status == 'Replied'){
		$('.inner-group-button').find("[data-label='Quotation']").hide();
	}

	cur_frm.add_custom_button(("Price Schedule"), function() {
		frappe.model.open_mapped_doc({
			method: "iac_electricals.iac_electricals.custom_scripts.lead.lead.make_price_schedule",
			frm : cur_frm
		})
	}, __("Create"));
}