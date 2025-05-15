# Copyright (c) 2025, taha ghabri and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum

def execute(filters dict  None = None)
	columns = get_columns()
	data = get_data()
	total_revenue = sum(row[revenue] for row in data)

	summary = [
		{
			label _(Total Revenue),
			value total_revenue,
			indicator green,
			datatype Currency
		}
	]

	chart = {
		type donut,
		data {
			labels [row[airline] for row in data],
			datasets [
				{
					name _(Revenue),
					values [row[revenue] for row in data]
				}
			]
		}
	}

	return columns, data, None, chart, summary

def get_columns() - list[dict]
	return [
		{
			label _(Airline),
			fieldname airline,
			fieldtype Link,
			options Airline,
			width 200
		},
		{
			label _(Revenue),
			fieldname revenue,
			fieldtype Currency,
			width 180
		}
	]

def get_data(filters=None)
	airlines = frappe.get_all(Airline, fields=[name])
	data = []

	AirplaneTicket = frappe.qb.DocType(Airplane Ticket)
	AirplaneFlight = frappe.qb.DocType(Airplane Flight)
	Airplane = frappe.qb.DocType(Airplane)

	for airline in airlines
		query = (
			frappe.qb.from_(AirplaneTicket)
			.join(AirplaneFlight).on(AirplaneTicket.flight == AirplaneFlight.name)
			.join(Airplane).on(AirplaneFlight.airplane == Airplane.name)
			.where((Airplane.airline == airline[name]) & (AirplaneTicket.docstatus == 1))
			.select(Sum(AirplaneTicket.total_amount).as_(total_revenue))
		)

		result = frappe.db.sql(query.get_sql(), as_dict=True)
		revenue = result[0].total_revenue or 0 if result else 0

		data.append({
			airline airline[name],
			revenue revenue
		})

	return data
