import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from dash import Dash, dcc, html, Input, Output, callback
from dash import dash_table
from collections import Counter


SAMPLE_late_delivery = pd.read_excel("Late Delivery Report Sample Data.xlsx")

print(SAMPLE_late_delivery.dtypes)

#Creating the calculated columns of Year, Month Name, Week of Month
SAMPLE_late_delivery["Date"]=SAMPLE_late_delivery["Date"].apply(lambda x: str(x).split(" ")[0])
SAMPLE_late_delivery["Date"]=pd.to_datetime(SAMPLE_late_delivery["Date"])
SAMPLE_late_delivery["Month Name"]=SAMPLE_late_delivery["Date"].dt.month_name()
SAMPLE_late_delivery["Year"]=SAMPLE_late_delivery["Date"].dt.year
SAMPLE_late_delivery["Week Number"] = SAMPLE_late_delivery["Date"].dt.day.apply(lambda x: "Week " + str((x-1)//7 + 1))

SAMPLE_late_delivery

# making the dash app

app = Dash(__name__)
server=app.server

app.layout = html.Div([
    html.H1("Sample Late Delivery Report"),
    html.H3("Sample Late Sunburst Report"),
    dcc.Dropdown(options=SAMPLE_late_delivery.columns,value=["Month Name","Week Number"],id="dropdown-1",multi=True),
    dcc.Graph(id="graph-1"),
    
    html.Br(),
    
    html.H3("Sample Word Cloud for Remarks of a Department"),
    dcc.Dropdown(options=SAMPLE_late_delivery["Reason of Delay"].unique(),value="Salesteam",id="dropdown-2"),
    dcc.Graph(id="graph-2")
    
])

@callback(

    Output("graph-1","figure"),
    Output("graph-2","figure"),
    Input("dropdown-1","value"),
    Input("dropdown-2","value")
    
)

def update_graph(value1,value2):
    
    fig=px.sunburst(SAMPLE_late_delivery,path=value1,width=1000,height=700)
    
    # Working for the wordcloud
    
    df_words = SAMPLE_late_delivery["Remark"][SAMPLE_late_delivery["Reason of Delay"]==value2]
   
    words= " ".join(i for i in df_words)
    words_dict=Counter(words.split(" "))
        
    fig2 = WordCloud(width=1000,height=700,background_color="white",stopwords=STOPWORDS,font_path=r"arial.ttf").generate(words)    
    fig_WC=px.imshow(fig2)
        
    return fig,fig_WC

if __name__=="__main__":
    app.run(debug=True)