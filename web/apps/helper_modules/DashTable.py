

import dash;
from dash.dependencies import Input, Output;
import dash_core_components as dcc;
import dash_html_components as html;




# reusable componenets
def make_dash_table(df):
	''' Return a dash definitio of an HTML table for a Pandas dataframe '''
	table = [];
	
	Tr_temp = [];
	for i in list(df.columns):
		if("cNIIOpt" in i):
			Tr_temp.append(html.Th([i],className="cNIIOpt"));
		elif("RiReMax" in i):
			Tr_temp.append(html.Th([i],className="RiReMax"));
		elif("STDMin" in i):
			Tr_temp.append(html.Th([i],className="STDMin"));
		else:
			Tr_temp.append(html.Th(i));

	table.append(html.Tr(Tr_temp));

	for index, row in df.iterrows():
			html_row = []
			for i in range(len(row)):
					html_row.append(html.Td([row[i]]))
			table.append(html.Tr(html_row))
	return table