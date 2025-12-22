# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
import csv

FILENAME = "data/processed_data.csv"


def loadDataAsList():
    salesData = []
    with open(FILENAME, newline='') as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            salesData.append(row)
    return salesData


def transformToLongForm(listData):
    salesData={"product": [], "sales": [], "date": [], "region": []}
    MEANSALES_BEFORE =0
    MEANSALES_BEFORE_COUNT = 0
    MEANSALES_AFTER=0
    MEANSALES_AFTER_COUNT=0
    price_increase_flag = False
    for i in range(1, len(listData)):
        salesData["product"].append(listData[i][0])
        salesData["sales"].append(float(listData[i][1]))
        salesData["date"].append(listData[i][2])
        salesData["region"].append(listData[i][3])
        if (not price_increase_flag) and listData[i][2] == "2021-01-15": 
            price_increase_flag=True
            print(price_increase_flag)
        if not price_increase_flag: 
            MEANSALES_BEFORE +=float(listData[i][1])
            MEANSALES_BEFORE_COUNT +=1
        else:
            MEANSALES_AFTER += float(listData[i][1])
            MEANSALES_AFTER_COUNT +=1
    print(MEANSALES_AFTER, MEANSALES_BEFORE)
    MEANSALES_BEFORE /= MEANSALES_BEFORE_COUNT
    MEANSALES_AFTER /= MEANSALES_AFTER_COUNT
    print(MEANSALES_AFTER, MEANSALES_BEFORE)
    return [salesData, MEANSALES_BEFORE, MEANSALES_AFTER]


app = Dash()


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#df = pd.DataFrame({
#    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#    "Amount": [4, 1, 2, 2, 4, 5],
#    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
#})

salesDataList = loadDataAsList()
data = transformToLongForm(salesDataList)
dataToDisplay = data[0]


df = pd.DataFrame(dataToDisplay)

fig = px.line(df, x="date", y="sales", line_group="region")
fig.add_vline(x = "2021-01-15", line_dash="dash")
fig.add_hline(y=data[1], line_dash="dash", line_color="red")
fig.add_hline(y=data[2], line_dash="dash", line_color="green")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Soul Foods: a visualisation of the January 15th 2021 price increase effect on 'pink morsels' sales.
    '''),

    html.Br(),
    html.Div(id="my-output"),
    html.Br(),
    html.Div([
        'Filter By Region ', 
        dcc.Dropdown(id='filter-by-region', options=['North', 'East','South', 'West', 'All'], value="All")
    ],style= {
        'width': 250
        }),

    dcc.Graph(
        id='example-graph',
        figure=fig,
    )
])

@callback(
    Output(component_id='example-graph', component_property='figure'),
    Input(component_id='filter-by-region', component_property='value')
)
def filterByRegion(region: str):
    filteredData=[]
    data=[]
    if region == "All" :
        data = transformToLongForm(salesDataList)
        fig = px.line(data[0], x="date", y="sales")
        fig.add_vline(x = "2021-01-15", line_dash="dash")
        fig.add_hline(y=data[1], line_dash="dash", line_color="red", annotation_text=f"${round(data[1], 2)} - Average sales before price increase", annotation_position="top right")
        fig.add_hline(y=data[2], line_dash="dash", line_color="green", annotation_text=f"${round(data[2], 2)} - Average sales after price increase", annotation_position="top left")
        return fig

    for row in salesDataList:
        if region.lower() == row[3]: filteredData.append(row)

    data = transformToLongForm(filteredData)
    fig = px.line(data[0], x="date", y="sales")
    fig.add_vline(x = "2021-01-15", line_dash="dash")
    fig.add_hline(y=data[1], line_dash="dash", line_color="red", annotation_text=f"${round(data[1], 2)} - Average sales before price increase", annotation_position="top right")
    fig.add_hline(y=data[2], line_dash="dash", line_color="green", annotation_text=f"${round(data[2], 2)} - Average sales after price increase", annotation_position="top left")
    return fig

if __name__ == '__main__':
    app.run(debug=True)
