# Copyright (c) 2025, taha ghabri and contributors
# For license information, please see license.txt

import frappe
from collections import defaultdict

def execute(filters=None):
	# table columns
	columns = [
		{
			"label": "Airline", 
			"fieldname": "airline", 
			"fieldtype": "Link", 
			"options": "Airline", 
			"width": 200
		},
		{
			"label": "Total Revenue", 
			"fieldname": "total_revenue", 
			"fieldtype": "Currency", 
			"width": 180
		}
	]

	tickets = frappe.get_all(
		"Airplane Ticket",
		filters={"docstatus": 1},
		fields=["total_amount", "flight"]
	)

	flights = frappe.get_all(
		"Airplane Flight",
		fields=["name", "airplane"]
	)
	flight_map = {f["name"]: f["airplane"] for f in flights}

	airplanes = frappe.get_all(
		"Airplane",
		fields=["name", "airline"]
	)
	airplane_map = {a["name"]: a["airline"] for a in airplanes}

	
	revenue_by_airline = defaultdict(float)
	for ticket in tickets:
		flight = flight_map.get(ticket["flight"])
		airline = airplane_map.get(flight)
		if airline:
			revenue_by_airline[airline] += float(ticket["total_amount"] or 0)

	data = [
		{"airline": airline, "total_revenue": total_revenue}
		for airline, total_revenue in revenue_by_airline.items()
	]
	data.sort(key=lambda x: x["total_revenue"], reverse=True)

	labels = [row["airline"] for row in data]
	values = [float(row["total_revenue"] or 0) for row in data]

	total_sum = sum(values)

	# Add a total row to the data
	data.append({
		"airline": "All Airlines",
		"total_revenue": total_sum
	})

	# report summary
	report_summary = [
		{
			"label": "Total Revenue (All Airlines)",
			"value": total_sum,
		}
	]

	# chart
	chart = {
		"data": {
			"labels": labels,
			"datasets": [
				{
					"name": "Total Revenue",
					"values": values,
				}
			]
		},
		"type": "pie"
	}

	return columns, data, f"<b>Total Revenue: {total_sum}</b>", chart, report_summary
