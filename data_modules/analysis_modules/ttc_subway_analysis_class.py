
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


	def Get_Live_TTC_Subway_Data(self):
		data = self._ttc_data_collector_obj.ttc_subway_data_collector();
		return data;






if __name__=="__main__":
	ttc_subway_analysis_obj = ttc_subway_analysis_class();
	data = ttc_subway_analysis_obj.Get_Live_TTC_Subway_Data();
	print(data)