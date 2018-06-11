"""
	Import Modules
"""
import dash, flask;
from dash.dependencies import Input, Output;
import dash_core_components as dcc;
import dash_html_components as html;
from flask import Flask, flash, redirect, render_template, request, session, abort
import os, sys;

sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '.', 'apps/ttc_subway_apps/')));
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data_modules/analysis_modules/')));

#################################### Import External Reporting Modules:
from ttc_subway_analysis_class import ttc_subway_analysis_class;

ttc_subway_analysis_obj = ttc_subway_analysis_class();
####################################


server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server)
app.config.suppress_callback_exceptions = True
app.title = 'TTC BUDDY'


#####################################
from subway_dashboard import subway_dashboard;
#####################################

sideBarAppList = [
					html.Div(
						className = "Template_LeftColumnSection",
						children = [html.H6("TTC BUDDY")]
					)
				]

app.layout = html.Div([
	dcc.Location(id='url', refresh=True),
	html.Div(id='page-content')
])

#####################################
subway_dashboard_obj = subway_dashboard(sideBarAppList, ttc_subway_analysis_obj);
subway_dashboard_obj.BindCallBackFunctions(app);
#####################################

# This is where we put the main
index_page = html.Div([
	html.Div(
		className="Template_Main row",
		children=[
			html.Div(
				className="Template_LeftColumn",
				children = sideBarAppList
			),
			html.Div(
				className="Template_RightColumn",
				children = []
			)
		]
	)
])






# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
			  [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/SubwayDashboard':
		return subway_dashboard_obj.Layout();
	else:
		return subway_dashboard_obj.Layout();


@server.route('/favicon.ico')
def favicon():
	return flask.send_from_directory(os.path.join(server.root_path, 'static'),'favicon.ico')



stylesheets = ["Index.css"];
for stylesheet in stylesheets:
	app.css.append_css({"external_url": "/static/css/{}".format(stylesheet)})

app.css.append_css({
	'external_url': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css'
})

external_js = ["https://code.jquery.com/jquery-3.3.1.min.js",
			 "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js",
			 "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.bundle.min.js"]
for js in external_js:
		app.scripts.append_script({"external_url": js})

internla_js = ["app.js","ajax.js"]
for js in internla_js:
		app.scripts.append_script({"external_url": "/static/js/{}".format(js)})


if __name__ == '__main__':
	app.run_server()