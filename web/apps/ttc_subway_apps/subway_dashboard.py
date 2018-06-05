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
import time;

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'helper_modules')));
from DashTable import *;

class subway_dashboard:

	def __init__(self, side_NavBar, ttc_subway_analysis_obj):
		self.side_NavBar = side_NavBar;
		self.ttc_subway_analysis_obj = ttc_subway_analysis_obj;

		ttcdata = self.ttc_subway_analysis_obj.Get_Live_TTC_Subway_Data();

		self.ttc_subway_map = self.MakeTTCSubwayMapWithNextTrain(ttcdata);
		self.ttc_filter_list = self.MakeTTCSubwayFilterList(ttcdata);

	def Layout(self):
		######################################################################################
		######################################################################################
		content = html.Div([
					dcc.Dropdown(
						id="MakeTTCSubwayFilterList",
						value = self.ttc_filter_list["value"],
						options = self.ttc_filter_list["options"],
						multi=False
					),
					html.Br([]),
					html.H6('TTC Subway Map - Next Train',className="gs-header gs-text-header padded"),
					dcc.Graph(
						id='TTCSubwayMapNextTrain',
						figure=self.ttc_subway_map,
						config={'displayModeBar': False}
					),
					html.Br([]),
					dcc.Graph(
						id='TTCSubwayMapNextTrainHistory',
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
		@appObj.callback(dash.dependencies.Output('TTCSubwayMapNextTrainHistory', 'figure'),[dash.dependencies.Input('MakeTTCSubwayFilterList', 'value')])
		def update_WIRP_PnLPlot(StationName):
			
			from_station = StationName.split("-towards-")[0].strip();
			to_station = StationName.split("-towards-")[1].strip();
			today_date = time.strftime('%Y%m%d');

			time_sample_list,delta_next_train_list = self.GetHistoricalDataAndProccessIt(from_station,to_station,today_date);



			data_to_plot = go.Scatter(
				x=time_sample_list,
				y=delta_next_train_list,
				mode = 'lines+markers',
				name='Minutes to Next Train'
			)
			data = [data_to_plot];
			layout = go.Layout(
				font=dict(color='#CCCCCC'),
				plot_bgcolor="#191A1A",
				paper_bgcolor="#020202",
				autosize=True,
				hovermode='closest',
				xaxis=dict(
					showgrid=True,
					zeroline=True,
					showline=True,
					mirror='ticks',
					gridcolor='#bdbdbd',
					gridwidth=0.5,
					zerolinecolor='#969696',
					zerolinewidth=0.5,
					linecolor='#636363',
					linewidth=0.5
				),
				yaxis=dict(
					showgrid=True,
					showline=True,
					gridcolor='#bdbdbd',
					range=[0, 10],
					title="Time to Next Train (min)",
					zeroline=True,
					mirror='ticks',
					gridwidth=0.5,
					zerolinecolor='#969696',
					zerolinewidth=0.5,
					linecolor='#636363',
					linewidth=0.5
				)
			)
			return go.Figure(data=data, layout=layout)



	def GetHistoricalDataAndProccessIt(self,from_station,to_station,today_date):
		data = self.ttc_subway_analysis_obj.GetHistoricalData(from_station,to_station,today_date);
		unique_time = list(set(list(data["collection_time"])));
		time_sample_list = [];
		delta_next_train_list = [];

		for i in unique_time:
			temp_DF = data[data["collection_time"] == i];

			collection_date = list(temp_DF["collection_date"])[1];
			departure_time_1 = list(temp_DF["departure_time"])[1];
			departure_time_2 = list(temp_DF["departure_time"])[2];

			departure_time_1 = datetime.strptime(collection_date+" "+departure_time_1, '%Y%m%d %H:%M:%S');
			departure_time_2 = datetime.strptime(collection_date+" "+departure_time_2, '%Y%m%d %H:%M:%S');

			delta_next_train = abs(departure_time_2 - departure_time_1);
			delta_next_train = str(delta_next_train);
			delta_next_train = delta_next_train.split(":");
			delta_next_train = float((float(delta_next_train[0])*60.0*60.0)+(float(delta_next_train[1]))+(float(delta_next_train[2])/60.0));

			time_sample_list.append(i);
			delta_next_train_list.append(delta_next_train);

		return time_sample_list,delta_next_train_list;










	def MakeTTCSubwayFilterList(self, ttcdata):
		from_station_name = list(ttcdata["current_station_name"]);
		to_station_name = list(ttcdata["to_station"]);
		station_direction_comb = [from_station_name[i]+" -towards- "+to_station_name[i] for i in range(len(from_station_name))];
		station_direction_comb = list(set(station_direction_comb));
		FilterList = {};
		FilterList["value"] = station_direction_comb[0];
		options = [];
		for i in station_direction_comb:
			temp = {};
			temp["label"] = i;
			temp["value"] = i;
			options.append(temp);
		FilterList["options"] = options;
		return FilterList;


	def MakeTTCSubwayMapWithNextTrain(self, ttcdata):
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

				collection_date = list(temp_DF["collection_date"])[0];
				collection_time = list(temp_DF["collection_time"])[0];
				collection_date_time = datetime.strptime(collection_date+" "+collection_time, '%Y%m%d %H:%M:%S');
				next_train_date_time = datetime.strptime(collection_date+" "+next_train, '%Y%m%d %H:%M:%S');
				delta_next_train = next_train_date_time - collection_date_time;
				delta_next_train = str(delta_next_train);
				delta_next_train = delta_next_train.split(":");
				delta_next_train = float((float(delta_next_train[0])*60.0*60.0)+(float(delta_next_train[1]))+(float(delta_next_train[2])/60.0));
		
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
						titleside='bottom'
					)
				)
			)
		]
		layout = go.Layout(
			font=dict(color='#CCCCCC'),
			plot_bgcolor="#191A1A",
			paper_bgcolor="#020202",
			autosize=True,
			hovermode='closest',
			mapbox=dict(
				accesstoken=mapbox_access_token,
				style="dark",
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
