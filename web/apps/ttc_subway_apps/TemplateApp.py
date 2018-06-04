"""
	Import Modules
"""
import os, sys;
import pandas as pd;
import dash;
import dash_core_components as dcc;
import dash_html_components as html;


sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../', 'helper_modules')));
from DashTable import *;

class Template:

	def __init__(self, side_NavBar):
		self.side_NavBar = side_NavBar;



	def Layout(self):
		######################################################################################
		######################################################################################
		content = None;
		######################################################################################
		######################################################################################
		layout = html.Div(
			className="Template_Main row",
			children=[
				html.Div(
					className="Template_LeftColumn",
					children = self.side_NavBar
				),
				html.Div(
					className="Template_RightColumn",
					children = [content]
				)
			]
		)

		return layout;



	def BindCallBackFunctions(self, appObj):
		pass;