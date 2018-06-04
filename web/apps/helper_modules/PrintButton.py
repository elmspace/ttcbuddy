import dash;
from dash.dependencies import Input, Output;
import dash_core_components as dcc;
import dash_html_components as html;

def print_button():
	printButton = html.A(['Print PDF'],className="button no-print print")
	return printButton