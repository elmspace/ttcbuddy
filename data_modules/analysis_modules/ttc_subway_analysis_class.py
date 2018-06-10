
import os, sys;
import json;

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'collection_modules/')));
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'database_modules/')));

from ttc_data_collector import ttc_data_collector;
from mysql_db import mysql_db;

class ttc_subway_analysis_class:

	def __init__(self):
		self._ttc_data_collector_obj = ttc_data_collector();
		self._mysql_db_obj = mysql_db();

	def GetMapBoxToken(self):
		_base_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../../', 'Configs/ttc_buddy/'));
		_config_data = _base_path+"/mapbox.json";
		with open(_config_data) as jsonFile:
			token = json.load(jsonFile);
		return token;

	def Get_Most_Recent_Data_From_DB(self):
		sql_query_condition = "where collection_date = (Select Max(collection_date) FROM ttc_buddy.ttc_subway_data) AND collection_time = (Select Max(collection_time) FROM ttc_buddy.ttc_subway_data where collection_date = (Select Max(collection_date) FROM ttc_buddy.ttc_subway_data) );"
		data = self._mysql_db_obj.Select_Data_with_Condition("ttc_subway_data",sql_query_condition);
		return data;


	def Get_Live_TTC_Subway_Data(self):
		data = self._ttc_data_collector_obj.ttc_subway_data_collector();
		return data;


	def GetHistoricalData(self, from_station, to_station, today_date):
		sql_query_condition = "where current_station_name ='"+str(from_station)+"' and to_station = '"+str(to_station)+"' and collection_date = '"+str(today_date)+"'";
		data = self._mysql_db_obj.Select_Data_with_Condition("ttc_subway_data",sql_query_condition);
		return data;



if __name__=="__main__":
	ttc_subway_analysis_obj = ttc_subway_analysis_class();
	data = ttc_subway_analysis_obj.Get_Most_Recent_Data_From_DB();
	print(data)