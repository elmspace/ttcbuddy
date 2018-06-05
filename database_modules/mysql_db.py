from sqlalchemy import create_engine;
import pandas as pd;
import os, sys;
import json;


class mysql_db:

	def __init__(self):
		_base_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../', 'Configs/ttc_buddy/'));
		_config_data = _base_path+"/sql_info.json";

		self._sql_config = self.Get_SQL_Config_Data(_config_data);
		_user = str(self._sql_config["user"]);
		_password = str(self._sql_config["password"]);
		_host = str(self._sql_config["host"]);
		_port = str(self._sql_config["port"]);
		_database = str(self._sql_config["database_name"]);

		self._sql_engine = create_engine('mysql://'+_user+':'+_password+'@'+_host+':'+_port+'/'+_database);




	def Get_SQL_Config_Data(self, input_ConfigPath):
		with open(input_ConfigPath) as jsonFile:
			connectionDetails = json.load(jsonFile);
		return connectionDetails;




	def Insert_Data(self, input_DataObject, input_TableName):
		input_DataObject.to_sql(input_TableName, self._sql_engine, if_exists='append', index=False);


	def Select_Data(self, input_TableName):
		connection = self._sql_engine.connect();
		sql_query = "Select * From "+str(input_TableName);
		data = pd.read_sql_query(sql_query, connection);
		return data;


	def Select_Data_with_Condition(self, input_TableName, input_Condition):
		connection = self._sql_engine.connect();
		sql_query = "Select * From "+str(input_TableName)+" "+input_Condition;
		data = pd.read_sql_query(sql_query, connection);
		return data;

if __name__=="__main__":
	pass;