import pandas as pd
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io
if not os.path.exists("OOP_\\images"):
    os.mkdir("OOP_\\images")
class MainDash:
    df = pd.read_csv('OOP_\\BTC__USD.csv', usecols=['Close', 'Date', 'Volume_BTC', 'Volume_USD'])

    def __init__(self, bt_bound, up_bound):
        #self.bt_bound = bt_bound
        #self.up_bound = up_bound
        filter1 = self.df[self.df.Date == up_bound].index[0]
        filter2 = self.df[self.df.Date == bt_bound].index[0]
        self.df = self.df.iloc[filter1-1 : filter2][::-1] #get an appropriate part of table

    def drawLineDash(self): #draw a line-graph
        fig = px.line(x = self.df.Date[::-1], y = self.df.Close[::-1]) #x:date; y:price
        fig.show()
        #fig.write_image("OOP_\\images\\fig1.png")
    def bubblePlot(self):
        fig = go.Figure(data=[go.Scatter(x = self.df.Date[::-1], y = self.df.Close[::-1],
                                         mode = 'markers',
                                         marker = dict(color = self.df.Volume_BTC/200 ,
                                                       size = self.df.Volume_BTC/100,
                                                       showscale = True))])
        fig.show() #x:Date; y:Price; color & size:Volume
        #fig.write_image("OOP_\\images\\fig2.png")

    def mixing(self):
        fig = px.bar(self.df, y='Close', x=self.df.Date, color='Volume_BTC', labels={'y': 'Close'},
                     hover_data=['Volume_BTC', 'Volume_USD'],
                     title='Evolution')
        fig.show() #x:Date; y:Price; color:Volume; prompted_data:'Volume_BTC', 'Volume_USD'
        fig.write_image("OOP_\\images\\fig3.png", engine = 'kaleido')

graph = MainDash("2018-09-27", "2019-03-27")
graph.drawLineDash()
graph.bubblePlot()
graph.mixing()



