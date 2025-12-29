# 1. imports of your dash app
from dash import Dash, html, dcc, Input, Output, callback
import app
import plotly.express as px
import pandas as pd
import csv
# 2. give each testcase a test case ID, and pass the fixture
# dash_duo as a function argument
def test_001_child_with_0(dash_duo):
    # 3. define your app inside the test function
    FILENAME = "data/processed_data.csv"

    #########################################
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

    ##########################################################
    app = Dash()
    salesDataList = loadDataAsList()
    data = transformToLongForm(salesDataList)
    dataToDisplay = data[0]


    df = pd.DataFrame(dataToDisplay)

    #Actual
    fig = px.line(df, x="date", y="sales", line_group="region")
    fig.add_vline(x = "2021-01-15", line_dash="dash")
    fig.add_hline(y=data[1], line_dash="dash", line_color="red")
    fig.add_hline(y=data[2], line_dash="dash", line_color="green")

    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Soul Foods: a visualisation of the January 15th 2021 price increase effect on 'pink morsels' sales.
        ''', id="header"),

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
    
    # 4. host the app locally in a thread, all dash server configs could be
    # passed after the first app argument
    dash_duo.start_server(app)
    # 5. use wait_for_* if your target element is the result of a callback,
    # keep in mind even the initial rendering can trigger callbacks
    dash_duo.wait_for_text_to_equal("#header",
    "Soul Foods: a visualisation of the January 15th 2021 price increase effect on 'pink morsels' sales.",
    timeout=4
    )
    dash_duo.wait_for_element("#example-graph", timeout=4)
    dash_duo.wait_for_element("#filter-by-region", timeout=400)
    dash_duo.multiple_click("#filter-by-region", 1)
    # 6. use this form if its present is expected at the action point
    #assert dash_duo.find_element("#nully-wrapper").text == "0"
    # 7. to make the checkpoint more readable, you can describe the
    # acceptance criterion as an assert message after the comma.
    # 8. visual testing with percy snapshot
    assert dash_duo.get_logs() == []
    # 8. visual testing with percy snapshot
    dash_duo.percy_snapshot("test_001_child_with_0-layout")
