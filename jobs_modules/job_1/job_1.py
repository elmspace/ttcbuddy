import os, sys;
import time;


sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data_modules/collection_modules/')));
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'database_modules/')));


from ttc_data_collector import ttc_data_collector;
from mysql_db import mysql_db;


ttc_data_collector_obj = ttc_data_collector();
mysql_db_obj = mysql_db();


for i in range(500):
	try:
		data = ttc_data_collector_obj.ttc_subway_data_collector();
		mysql_db_obj.Insert_Data(data,"ttc_subway_data");
		print("loading");
		time.sleep(60);
	except Exception as e:
		print("error");
		pass;



# data = mysql_db_obj.Select_Data("ttc_subway_data");
# current_date = data["current_date"];
# current_date = [i.replace("-","") for i in current_date];
# data["current_date"] = current_date;
# print(data.head());
# mysql_db_obj.Insert_Data(data,"ttc_subway_data_cp");