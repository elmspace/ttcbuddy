import pandas as pd;
import os, sys;
import time;
from pytz import timezone;
from datetime import datetime;


sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'api_modules/ttc_api')));
from ttc_api import ttc_api;

class ttc_data_collector:


	def __init__(self):
		self._ttc_api_obj = ttc_api();



	def ttc_subway_data_collector(self):
		thingsToRemove = ["Station","Platform","Subway","Northbound","Eastbound","Westbound","Southbound"];

		ttc_api_obj = self._ttc_api_obj;

		service_lines = ["yonge-university-spadina_subway","sheppard_subway","bloor-danforth_subway","scarborough_rt"];

		subway_data_main = pd.DataFrame(columns=["current_station_uri","current_station_name","lat","lng","to_station","departure_time","collection_time","collection_date"]);

		fmt_date = '%Y%m%d';
		fmt_time = '%H:%M:%S';
		fmt_time_id = '%H%M%S';
		eastern = timezone('US/Eastern');
		loc_dt = datetime.now(eastern);
		collection_date_val = loc_dt.strftime(fmt_date);
		collection_time_val = loc_dt.strftime(fmt_time);
		collection_id_val = int(loc_dt.strftime(fmt_date)+loc_dt.strftime(fmt_time_id));

		for service_line in service_lines:

			station_names = [];
			station_lat = [];
			station_lng = [];
			station_pretty_name = [];
			api_data = ttc_api_obj.api_get_ttc_info(service_line);
			for i in api_data["shapes"][0]["stops"]:
				station_names.append(i["uri"].split("#")[0]);
				station_lat.append(i["lat"]);
				station_lng.append(i["lng"]);
				station_pretty_name.append(i["name"].replace("Station","").replace("Platform","").replace("Subway","").strip());

			subway_data = pd.DataFrame(columns=["collection_id","current_station_uri","current_station_name","lat","lng","to_station","departure_time","collection_time","collection_date"]);

			current_station = [];
			to_station = [];
			departure_time = [];
			collection_time = [];
			collection_date = [];
			current_lat = [];
			current_lng = [];
			current_pretty_name = [];
			collection_id = [];

			for count in range(len(station_names)):
				name = station_names[count];
				lat = station_lat[count];
				lng = station_lng[count];
				pretty_name = station_pretty_name[count];

				api_data = ttc_api_obj.api_get_ttc_info(name);
				for i in api_data["stops"]:
					for j in i["routes"]:
						if(j["route_group_id"]=="1" or j["route_group_id"]=="2" or j["route_group_id"]=="3" or j["route_group_id"]=="4"):
							for k in j["stop_times"]:
								current_station.append(name);
								current_lat.append(lat);
								current_lng.append(lng);
								current_pretty_name.append(pretty_name);
								to_station_value = k["shape"].split("To")[1].strip();
								for removeThese in thingsToRemove:
									to_station_value.replace(removeThese,"");
								to_station.append(to_station_value.strip());
								departure_time_val = time.strftime('%H:%M:%S', time.localtime(int(k["departure_timestamp"])))
								fmt = "%H:%M:%S";
								t = datetime.fromtimestamp(float(k["departure_timestamp"]),eastern);
								departure_time_val = t.strftime(fmt);
								departure_time.append(departure_time_val);
								collection_time.append(collection_time_val);
								collection_date.append(collection_date_val);
								collection_id.append(collection_id_val);

			subway_data["current_station_uri"] = current_station;
			subway_data["to_station"] = to_station;
			subway_data["departure_time"] = departure_time;
			subway_data["collection_time"] = collection_time;
			subway_data["collection_date"] = collection_date;
			subway_data["current_station_name"] = current_pretty_name;
			subway_data["lat"] = current_lat;
			subway_data["lng"] = current_lng;
			subway_data["collection_id"] = collection_id;


			subway_data_main = subway_data_main.append(subway_data);

		return subway_data_main;



# if __name__=="__main__":
# 	ttc_data_collector_obj = ttc_data_collector();
# 	print(ttc_data_collector_obj.ttc_subway_data_collector());