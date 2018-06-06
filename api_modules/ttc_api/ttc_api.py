
import json;
import urllib.request;


class ttc_api:

	def __init__(self):
		self._base_ttc_api_url = "http://myttc.ca/";


	def api_get_ttc_info(self, input_station, input_data_type = "json"):
		station_url = self._base_ttc_api_url + input_station + "." +input_data_type;
		webURL = urllib.request.urlopen(station_url);
		data = webURL.read();
		encoding = webURL.info().get_content_charset('utf-8');
		response = json.loads(data.decode(encoding));

		return response;




