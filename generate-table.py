import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from qsweepy import database
from pony.orm import *

#df = pd.read_csv(
#    'https://gist.githubusercontent.com/chriddyp/'
#    'c78bf172206ce24f77d6363a2d754b59/raw/'
#    'c353e8ef842413cae56ae3920b8fd78468aa4cb2/'
#    'usa-agricultural-exports-2011.csv')

def data_to_dict(data):
	return { 'id': data.id,
			 'comment': data.comment,
			 'sample_name': data.sample_name,
			 'time_start': data.time_start,
			 'time_stop': data.time_stop,
			 'filename': data.filename,
			 'type_revision': data.type_revision,
			 'incomplete': data.incomplete,
			 'invalid': data.invalid,
			 'owner': data.owner,
			} 

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(str(dataframe.iloc[i][col])) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

db = database.database()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
@db_session
def get_databases():
	databases = list(data_to_dict(x) for x in list(select(c for c in db.Data)))
	return pd.DataFrame(databases)
df = get_databases()

app.layout = html.Div(children=[
	html.H4(children='Measurements'),
	generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)