frappe.provide("pni.dashboard");

frappe.pages['pni-dashboard'].on_page_load = function(wrapper) {
	new pni.dashboard.paperCup(wrapper)
}

pni.dashboard.paperCup = class paperCup
{
	constructor(wrapper) {
		var page = frappe.ui.make_app_page({
			parent: wrapper,
			title: 'PNI Dashboard',
			single_column: true
		});
		this.parent = wrapper;
		this.page = this.parent.page;

		this.make();
	}
	make() {
		
		const me = this;

		me.$main_section = $(`<div class="reconciliation page-main-content"></div>`).appendTo(me.page.main);
		
		
		const empty_state = __("Upload a bank statement, link or reconcile a bank account")
		
		me.$main_section.append(`
			<div>
				<div class="myDIV">
					<table>
					<tr>
					<td bgcolor="#9ac36a">Uncoated Reel</td>
					</tr>
					<tr>
					<td id="uncoated">value</td>
					</tr>
					<table>
				</div>
				<div class="myDIV">
					<table>
					<tr>
					<td bgcolor="#2196f3">LDPE</td>
					</tr>
					<tr>
					<td id="ldpe">value</td>
					</tr>
					<table>
				</div>
				<div class="myDIV">
					<table>
					<tr>
					<td bgcolor="#ffc107">INK</td>
					</tr>
					<tr>
					<td id="ink">value</td>
					</tr>
					<table>
				</div>
				<div class="myDIV">
					<table>
					<tr>
					<td bgcolor="#2fc1b4">Blank Production</td>
					</tr>
					<tr>
					<td id="blank">value</td>
					</tr>
					<table>
				</div>
				<div >
					<table>
					<tr>
					<td bgcolor="#FF5722">Bottom Production</td>
					</tr>
					<tr>
					<td id="bottom">value</td>
					</tr>
					<table>
				</div>
				<div >
					<table>
					<tr>
					<td bgcolor="#e91e63">Paper Cup Production</td>
					</tr>
					<tr>
					<td id="paper">value</td>
					</tr>
					<table>
				</div>
			</div>
			<style>
				table,tr,td{
				border: 1px solid #c5bcbc;
				border-collapse: collapse;
				height:30px;
				width:150px;
				text-align:center;

				}
				.myDIV {
				 float:left;
				//  display:flex;

				}
			</style>
		`)

		$( document ).ready(function() {
			frappe.xcall('pni_report_dashboard.pni_report_dashboard.page.pni_dashboard.pni_dashboard.get_cup_production',{item_group: "paper reel"})
			.then((result) => {
				$("#uncoated").html(result);
			})
			frappe.xcall('pni_report_dashboard.pni_report_dashboard.page.pni_dashboard.pni_dashboard.get_ldpe')
			.then((result) => {
				$("#ldpe").html(result);
			})
			frappe.xcall('pni_report_dashboard.pni_report_dashboard.page.pni_dashboard.pni_dashboard.get_ink',{item_group: "Printing INK"})
			.then((result) => {
				$("#ink").html(result);
			})

			frappe.xcall('pni_report_dashboard.pni_report_dashboard.page.pni_dashboard.pni_dashboard.get_cup_production',{item_group: "Paper Blank"})
			.then((result) => {
				$("#blank").html(result);
			})

			frappe.xcall('pni_report_dashboard.pni_report_dashboard.page.pni_dashboard.pni_dashboard.get_cup_production',{item_group: "Paper Cup"})
			.then((result) => {
				$("#paper").html(result);
			})

			frappe.xcall('pni_report_dashboard.pni_report_dashboard.page.pni_dashboard.pni_dashboard.get_cup_production',{item_group: "Paper Bottom"})
			.then((result) => {
				$("#bottom").html(result);
			})
		})

		
	}

}