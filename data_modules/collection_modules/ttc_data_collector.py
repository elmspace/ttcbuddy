import pandas as pd;
import os, sys;
import time;


sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'api_modules/ttc_api')));
from ttc_api import ttc_api;

class ttc_data_collector:


	def __init__(self):
		self._ttc_api_obj = ttc_api();


	def ttc_subway_data_collector(self):
		ttc_api_obj = self._ttc_api_obj;
		station_names = [];
		station_lat = [];
		station_lng = [];
		station_pretty_name = [];
		api_data = ttc_api_obj.api_get_ttc_info("yonge-university-spadina_subway");
		for i in api_data["shapes"][0]["stops"]:
			station_names.append(i["uri"].split("#")[0]);
			station_lat.append(i["lat"]);
			station_lng.append(i["lng"]);
			station_pretty_name.append(i["name"].replace("Station","").replace("Platform","").replace("Subway","").strip());
  
		subway_data = pd.DataFrame(columns=["current_station_uri","current_station_name","lat","lng","to_station","departure_time","current_time","current_date"]);

		current_station = [];
		to_station = [];
		departure_time = [];
		current_time = [];
		current_date = [];
		current_lat = [];
		current_lng = [];
		current_pretty_name = [];

		current_time_val = time.strftime('%H:%M:%S');
		current_date_val = time.strftime('%Y-%m-%d');

		for count in range(len(station_names)):
			name = station_names[count];
			lat = station_lat[count];
			lng = station_lng[count];
			pretty_name = station_pretty_name[count];

			api_data = ttc_api_obj.api_get_ttc_info(name);
			for i in api_data["stops"]:
				for j in i["routes"]:
					if(j["route_group_id"]=="1" or j["route_group_id"]=="2"):
						for k in j["stop_times"]:
							current_station.append(name);
							current_lat.append(lat);
							current_lng.append(lng);
							current_pretty_name.append(pretty_name);
							to_station.append(k["shape"].split("To")[1].strip().replace("Station","").replace("Platform","").replace("Subway","").strip());
							departure_time_val = time.strftime('%H:%M:%S', time.localtime(int(k["departure_timestamp"])))
							departure_time.append(departure_time_val);
							current_time.append(current_time_val);
							current_date.append(current_date_val);

		subway_data["current_station_uri"] = current_station;
		subway_data["to_station"] = to_station;
		subway_data["departure_time"] = departure_time;
		subway_data["current_time"] = current_time;
		subway_data["current_date"] = current_date;
		subway_data["current_station_name"] = current_pretty_name;
		subway_data["lat"] = current_lat;
		subway_data["lng"] = current_lng;

		return subway_data;