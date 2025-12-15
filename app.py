# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import csv

FILENAME = "data/processed_data.csv"

def loadData():
    salesData={"product": [], "sales": [], "date": []}
    with open(FILENAME, newline='') as csvfile:
        filereader = csv.DictReader(csvfile)
        for row in filereader:
            salesData["product"].append(row["product"])
            salesData["sales"].append(float(row["sales"]))
            salesData["date"].append(row["date"])
            
    return salesData

app = Dash()


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#df = pd.DataFrame({
#    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#    "Amount": [4, 1, 2, 2, 4, 5],
#    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
#})

data = loadData()

df = pd.DataFrame(data)

fig = px.line(df, x="date", y="sales")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
