import pandas as pd
import numpy as np
import plotly.tools as tls
import plotly.express as px
import plotly.graph_objects as go

class MainDash:
    df = pd.read_csv('OOP_\\BTC__USD.csv', usecols=['Close', 'Date', 'Volume_BTC'])[::-1]
    def __init__(self, bt_bound, up_bound):
        self.bt_bound = bt_bound
        self.up_bound = up_bound
        self.df = self.df.iloc[self.bt_bound : self.up_bound]
    def drawLineDash(self):
        fig = px.line(x = self.df.Date[::-1], y = self.df.Close[::-1])
        fig.show()

    def bubblePlot(self):
        fig = go.Figure(data=[go.Scatter(x = self.df.Close[::-1], y = self.df.Date[::-1],
                                         mode = 'markers',
                                         marker = dict(color = self.df.Volume_BTC/200 ,
                                                       size = self.df.Volume_BTC/100,
                                                       showscale = True))])
        fig.show()

    def mixing(self):
        fig = px.bar(self.df, y='Close', x=self.df.Date, color='Volume_BTC', labels={'y': 'Close'},
                     hover_data=['Close'],
                     title='Evolution')
        fig.show()

graph = MainDash(10, 80)
graph.drawLineDash()
graph.bubblePlot()
graph.mixing()

# Bar Graph for DataFrame
# fig = go.Figure(data=go.Bar(x = list(df.Date), y=list(df.Price)))
# fig.show()

# Table with graphics
# fig = go.Figure(data=[go.Table(header=dict(values=list(df.columns),
#                 fill_color='paleturquoise',align='left'),
#                 cells=dict(values=[df.Date, df.Price],
#                 fill_color='lavender', align='left'))
# ])
# fig.show()


