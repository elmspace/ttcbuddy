"""
	Import Modules
"""
import os, sys;
import pandas as pd;
import dash;
import dash_core_components as dcc;
import dash_html_components as html;
import plotly.plotly as py;
import plotly.graph_objs as go;
from datetime import datetime;

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'helper_modules')));
from DashTable import *;

class subway_dashboard:

	def __init__(self, side_NavBar, ttc_subway_analysis_obj):
		self.side_NavBar = side_NavBar;
		self.ttc_subway_analysis_obj = ttc_subway_analysis_obj;

		self.ttc_subway_map = self.MakeTTCSubwayMapWithNextTrain();

	def Layout(self):
		######################################################################################
		######################################################################################
		content = html.Div([
					html.H6('TTC Subway Map - Next Train',className="gs-header gs-text-header padded"),
					dcc.Graph(
						id='PnLAnalysisPlot',
						figure=self.ttc_subway_map,
						config={'displayModeBar': False}
					)
				]);
		######################################################################################
		######################################################################################
		layout = html.Div(
			className="Template_Main row",
			children=[
				html.Div(
					className="Template_LeftColumn",
					children = self.side_NavBar
				),
				html.Div(
					className="Template_RightColumn",
					children = [content]
				)
			]
		)

		return layout;



	def BindCallBackFunctions(self, appObj):
		pass;





	def MakeTTCSubwayMapWithNextTrain(self):
		ttcdata = self.ttc_subway_analysis_obj.Get_Live_TTC_Subway_Data();

		from_station = list(ttcdata["current_station_name"]);
		to_station = list(ttcdata["to_station"]);
		unq_comb = list(set([i+"~"+j for i in from_station for j in to_station]));
		
		lat_list = [];
		lng_list = [];
		text_list = [];
		delta_time_list = [];
		for i in unq_comb:
			try:
				temp_DF = ttcdata[(ttcdata["current_station_name"]==i.split("~")[0]) & (ttcdata["to_station"]==i.split("~")[1])];
				lat_val = list(temp_DF["lat"])[0];
				lng_val = list(temp_DF["lng"])[0];
				next_train = list(temp_DF["departure_time"])[0];
				station_name = list(temp_DF["current_station_name"])[0];
				to_station = list(temp_DF["to_station"])[0];

				current_date = list(temp_DF["current_date"])[0];
				current_time = list(temp_DF["current_time"])[0];
				current_date_time = datetime.strptime(current_date+" "+current_time, '%Y-%m-%d %H:%M:%S');
				next_train_date_time = datetime.strptime(current_date+" "+next_train, '%Y-%m-%d %H:%M:%S');
				delta_next_train = next_train_date_time - current_date_time;
				delta_next_train = str(delta_next_train);
				delta_next_train = delta_next_train.split(":");
				delta_next_train = int((float(delta_next_train[0])*60.0*60.0)+(float(delta_next_train[1])*60.0)+(float(delta_next_train[2])));
		
				delta_time_list.append(delta_next_train);
				lat_list.append(lat_val);
				lng_list.append(lng_val);
				text_list.append("From: "+str(station_name)+" To: "+str(to_station)+" Next Train: "+str(next_train));
			except Exception as e:
				pass;

		data = self.ttc_subway_analysis_obj.GetMapBoxToken();
		mapbox_access_token = data["token"]
	
		data = [
			go.Scattermapbox(
				lat=lat_list,
				lon=lng_list,
				text=text_list,
				mode='markers',
				marker=dict(
					colorscale= "Reds",
					color = delta_time_list,
					size=9,
					colorbar = dict(
						titleside='right'
					)
				)
			)
		]
		layout = go.Layout(
			autosize=True,
			hovermode='closest',
			mapbox=dict(
				accesstoken=mapbox_access_token,
				bearing=0,
				center=dict(
					lat=43.7057304382,
					lon=-79.398475646999998
				),
				pitch=0,
				zoom=10
			),
			margin=go.Margin(
				l=0,
				r=0,
				b=0,
				t=0,
				pad=0
			)
		)
		return go.Figure(data=data, layout=layout);



##############################################
if __name__=="__main__":

	sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../../', 'data_modules/analysis_modules/')));
	from ttc_subway_analysis_class import ttc_subway_analysis_class;
	ttc_subway_analysis_obj = ttc_subway_analysis_class();

	subway_dashboard_obj = subway_dashboard(None,ttc_subway_analysis_obj);
	print(subway_dashboard_obj.ttc_subway_map)