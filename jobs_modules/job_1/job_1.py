import os, sys;
import time;


sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'data_modules/collection_modules/')));
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'database_modules/')));


from ttc_data_collector import ttc_data_collector;
from mysql_db import mysql_db;


ttc_data_collector_obj = ttc_data_collector();
mysql_db_obj = mysql_db();


for i in range(500):
	data = ttc_data_collector_obj.ttc_subway_data_collector();
	mysql_db_obj.Insert_Data(data,"ttc_subway_data");
	print("loading");
	time.sleep(60*3);


# data = mysql_db_obj.Select_Data("ttc_subway_data");
# print(data.head());