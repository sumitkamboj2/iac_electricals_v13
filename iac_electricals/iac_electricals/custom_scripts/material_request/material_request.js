frappe.ui.form.on("Material Request", {
	project: function(frm, cdt, cdn) {
		if(!frm.doc.delivery_date) {
			erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "project");
		}
	}
})
