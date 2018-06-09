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
from pytz import timezone;
import time;

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'helper_modules')));
from DashTable import *;

class subway_dashboard:

	def __init__(self, side_NavBar, ttc_subway_analysis_obj):
		self.side_NavBar = side_NavBar;
		self.ttc_subway_analysis_obj = ttc_subway_analysis_obj;

		self.ttcdata = self.ttc_subway_analysis_obj.Get_Live_TTC_Subway_Data();

		self.ttc_subway_map = self.MakeTTCSubwayMapWithNextTrain();
		self.ttc_filter_list = self.MakeTTCSubwayFilterList();

	def Layout(self):
		######################################################################################
		######################################################################################
		content = html.Div([
					html.Div(id="fakeDiv",children=[]),
					html.Div(className="rowSection row", children=[
						html.Div(className="leftSection",children=[
							html.H6('Select a Station:',className="gs-header gs-text-header padded"),
							dcc.Dropdown(
								id="MakeTTCSubwayFilterList",
								value = self.ttc_filter_list["value"],
								options = self.ttc_filter_list["options"],
								multi=False
							)
						]),
						html.Div(className="rightSection",children=[
							html.H6('Next Departure Time:',className="gs-header gs-text-header padded"),
							html.Div(id="NextTrainDataTable")
						])
					]),
					html.Div(className="rowSection row", children=[
						html.Div(className="leftSection",children=[
							html.H6('TTC Subway Map - Next Train',className="gs-header gs-text-header padded"),
							dcc.Graph(
								id='TTCSubwayMapNextTrain',
								figure=self.ttc_subway_map,
								config={'displayModeBar': False}
							)
						]),
						html.Div(className="rightSection",children=[
							html.H6("Today's Performance",className="gs-header gs-text-header padded"),
							dcc.Graph(
								id='TTCSubwayMapNextTrainHistory',
								config={'displayModeBar': False}
							)
						])
					])
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

		@appObj.callback(dash.dependencies.Output('fakeDiv', 'children'),[dash.dependencies.Input('MakeTTCSubwayFilterList', 'value')])
		def Update_Data(StationName):
			self.ttcdata = self.ttc_subway_analysis_obj.Get_Live_TTC_Subway_Data();


		@appObj.callback(dash.dependencies.Output('TTCSubwayMapNextTrainHistory', 'figure'),[dash.dependencies.Input('MakeTTCSubwayFilterList', 'value')])
		def Update_Historical_Station_Data(StationName):
			data = [];
			from_station = StationName.split("-towards-")[0].strip();
			to_station = StationName.split("-towards-")[1].strip();
			
			fmt = '%Y%m%d';
			eastern = timezone('US/Eastern');
			loc_dt = datetime.now(eastern);
			today_date = loc_dt.strftime(fmt);
						
			time_sample_list,delta_next_train_list = self.GetHistoricalDataAndProccessIt(from_station,to_station,today_date);
			data_to_plot = go.Scatter(
				x=time_sample_list,
				y=delta_next_train_list,
				mode = 'lines',
				name= from_station
			)
			data.append(data_to_plot);
			layout = go.Layout(
				font=dict(color='#CCCCCC'),
				plot_bgcolor="black",
				paper_bgcolor="black",
				autosize=True,
				hovermode='closest',
				xaxis=dict(),
				yaxis=dict(
					title="Time to Next Train (min)",
					zeroline=True,
					mirror='ticks',
					zerolinecolor='#969696',
					linecolor='#636363',
				)
			)
			return go.Figure(data=data, layout=layout)


		@appObj.callback(dash.dependencies.Output('NextTrainDataTable', 'children'),[dash.dependencies.Input('MakeTTCSubwayFilterList', 'value')])
		def Update_Next_Train_Data(StationName):
			from_station = StationName.split("-towards-")[0].strip();
			to_station = StationName.split("-towards-")[1].strip();
			
			TableData = self.ttcdata[(self.ttcdata["current_station_name"]== from_station) & (self.ttcdata["to_station"]== to_station)];

			columnsToKeep = ["current_station_name" , "to_station" , "departure_time"];
			TableData = TableData[columnsToKeep];
			TableData.columns = ["From","Towards","Departure Time"];

			return html.Table(make_dash_table(TableData),className="darkTable")



		@appObj.callback(dash.dependencies.Output('TTCSubwayMapNextTrain', 'figure'),[dash.dependencies.Input('MakeTTCSubwayFilterList', 'value')])
		def Update_Next_Train_Map(StationName):
			return self.MakeTTCSubwayMapWithNextTrain(StationName);





	def GetHistoricalDataAndProccessIt(self,from_station,to_station,today_date):
		data = self.ttc_subway_analysis_obj.GetHistoricalData(from_station,to_station,today_date);
		unique_time = list(set(list(data["collection_time"])));
		time_sample_list = [];
		delta_next_train_list = [];
		unique_time.sort()

		next_train_collection_date = [];
		next_train_collection_time = [];
		next_train_time_list = [];
		for i in unique_time:
			temp_DF = data[data["collection_time"] == i];

			next_train_at = list(temp_DF["departure_time"])[0];
			collection_date_val = list(temp_DF["collection_date"])[0];
			if((next_train_at in next_train_time_list)==False):
				next_train_time_list.append(next_train_at);
				next_train_collection_date.append(collection_date_val);
				next_train_collection_time.append(i);

		next_train_delta_time_list = [];
		for i in range(len(next_train_time_list)-1):
			t0 = next_train_time_list[i];
			t1 = next_train_time_list[i+1];
			t0 = datetime.strptime(next_train_collection_date[i]+" "+t0, '%Y%m%d %H:%M:%S');
			t1 = datetime.strptime(next_train_collection_date[i]+" "+t1, '%Y%m%d %H:%M:%S');

			delta_next_train = abs(t1 - t0);
			delta_next_train = str(delta_next_train);
			delta_next_train = delta_next_train.split(":");
			delta_next_train = float((float(delta_next_train[0])*60.0*60.0)+(float(delta_next_train[1]))+(float(delta_next_train[2])/60.0));

			if(abs(delta_next_train) < 50.0):
				time_sample_list.append(next_train_collection_time[i]);
				delta_next_train_list.append(delta_next_train);


		return time_sample_list,delta_next_train_list;










	def MakeTTCSubwayFilterList(self):
		ttcdata = self.ttcdata;
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
		FilterList["station_dest_list"] = station_direction_comb;

		return FilterList;


	def MakeTTCSubwayMapWithNextTrain(self, selectedStation = None):
		ttcdata = self.ttcdata;
		if(selectedStation):
			selectedStation = selectedStation.split("-towards-")[0].strip();
		from_station = list(ttcdata["current_station_name"]);
		to_station = list(ttcdata["to_station"]);
		unq_comb = list(set([i+"~"+j for i in from_station for j in to_station]));
		
		lat_list = [];
		lng_list = [];
		text_list = [];
		delta_time_list = [];

		selected_lat_list = [];
		selected_lng_list = [];
		selected_text_list = [];
		selected_delta_time_list = [];
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
		

				if(selectedStation):
					if(selectedStation in i.split("~")[0]):
						selected_delta_time_list.append(delta_next_train);
						selected_lat_list.append(lat_val);
						selected_lng_list.append(lng_val);
						selected_text_list.append("From: "+str(station_name)+" To: "+str(to_station)+" Next Train: "+str(next_train));
					else:
						delta_time_list.append(delta_next_train);
						lat_list.append(lat_val);
						lng_list.append(lng_val);
						text_list.append("From: "+str(station_name)+" To: "+str(to_station)+" Next Train: "+str(next_train));
				else:
					delta_time_list.append(delta_next_train);
					lat_list.append(lat_val);
					lng_list.append(lng_val);
					text_list.append("From: "+str(station_name)+" To: "+str(to_station)+" Next Train: "+str(next_train));

			except Exception as e:
				pass;

		data = self.ttc_subway_analysis_obj.GetMapBoxToken();
		mapbox_access_token = data["token"]
	

		if(selectedStation):
			data = [
				go.Scattermapbox(
					lat=lat_list,
					lon=lng_list,
					text=text_list,
					mode='markers',
					name="",
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
			data += [
				go.Scattermapbox(
					lat=selected_lat_list,
					lon=selected_lng_list,
					text=selected_text_list,
					mode='markers',
					name="",
					marker=dict(
						colorscale= "Reds",
						color = selected_delta_time_list,
						size=30,
						colorbar = dict(
							titleside='bottom'
						)
					)
				)
			]
		else:
			data = [
				go.Scattermapbox(
					lat=lat_list,
					lon=lng_list,
					text=text_list,
					mode='markers',
					name="",
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
			showlegend=False,
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
