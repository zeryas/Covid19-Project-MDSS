#!/usr/bin/env python
# coding: utf-8

# In[2]:


import plotly.graph_objects as go 
import matplotlib.pyplot as plt
import numpy as np
import dash 
import datetime as dt 
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output


# In[3]:


df = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7', sep = ';')
df = df.dropna()
df.index = df['jour'] # mettre en index les jours des pays
df = df.drop(['jour'], axis=1) # enlever la colonne jour dupliqué


# In[ ]:


import plotly.express as px
app = dash.Dash()
server = app.server

### TRACES plots 
trace1 = px.line( df,
    x=df.index,  
    y=df['hosp']
)

trace2 = px.line( df,
    x=df.index,  
    y=df['dc']
)


### defining HTML content 
app.layout = html.Div([
    html.Div([
        html.H1("Covid19 DashBoard Application On French Data")], style={'marginLeft':50}, 
        className="banner"),


    html.Div(children= [dcc.Dropdown(id="variable",
                 options=[
                     {"label": "Morts",             "value": 'dc'},
                     {"label": "Réanimation",       "value": 'rea'},
                     {"label": "Retour à domicil",  "value": 'rad'},
                     {"label": "Hospitalisation",   "value": 'hosp'},
                 ],
                 multi=False,
                 value= 'dc',
                 style={'width': '100%'}
                 ),
                       dcc.Graph(id='line-plot')], 
         style = {'width': '60%', 'display' : 'inline-block'} ),
  #############################################################################################
    html.Div(children=[dcc.Dropdown(id="var",
                 options=[
                     {"label": "Morts",             "value": 'dc'},
                     {"label": "Réanimation",       "value": 'rea'},
                     {"label": "Retour à domicil",  "value": 'rad'},
                     {"label": "Hospitalisation",   "value": 'hosp'},
                 ],
                 multi=False,
                 value= 'dc',
                 style={'width': '100%'}
                 ),
             dcc.Graph(id='plot')],
             style = {'width': '40%', 'display' : 'inline-block'} ),
    #########################################################################################
      html.Div(children=[dcc.Dropdown(id='dep', 
                                      options=[{'label':'Paris, Ile de France' , 'value': '75'},
                                                        {'label': 'Val de Marne', 'value': '94'},
                                                        {'label': 'Rhon', 'value': '69'},
                                                        {'label': 'Moselle', 'value': '57'},
                                                        {'label': 'Nord', 'value': '59'}], 

                                      multi=False, 
                                      value= '59', 
                                      style={'width': '100%'}),
                 dcc.Graph(id='graph')],
                 style = {'width': '60%', 'display' : 'inline-block'})
])
    
# callbacks TO UPDATE GRAPHIC
############################################################################################
@app.callback(Output(component_id='line-plot', component_property='figure'),
              [Input(component_id='variable',component_property='value')])

def plot_line(variable):
    if variable == 'dc':
        fig={
            'data': [
                go.Bar(
                   x=df.index,  
                   y=df['dc']
                )],
            'layout': go.Layout(
                title = 'Nombre de décès en France',
                xaxis = {'title': 'Days'},
                yaxis = {'title': 'Number of death'},
                hovermode='closest'
            )}
    elif variable == 'hosp':
        fig={
            'data': [
                go.Bar(
                   x=df.index,  
                   y=df['hosp']
                )],
            'layout': go.Layout(
                title = 'Hospitalisation',
                xaxis = {'title': 'Jours'},
                yaxis = {'title': 'hospitalisations'},
                hovermode='closest'
            )}
    elif variable == 'rad':
        fig={
            'data': [
                go.Bar(
                    x=df.index,  # NOC stands for National Olympic Committee
                    y=df['rad']
                )],
            'layout': go.Layout(
                title = 'Nombre des retours à domicile',
                xaxis = {'title': 'Jours'},
                yaxis = {'title': 'Retour à domicile'},
                hovermode='closest'
            )}
    elif variable == 'rea':
        fig={
            'data': [
                go.Bar(
                    x=df.index,  # NOC stands for National Olympic Committee
                    y=df['rea']
                )],
            'layout': go.Layout(
                title = 'Nombre de patients en Réanimation',
                xaxis = {'title': 'Jours'},
                yaxis = {'title': 'Patients en réanimation'},
                hovermode='closest'
            )}

    return fig
#################################################################################################
@app.callback(
    Output(component_id='plot', component_property='figure'),
   [Input(component_id='var',component_property='value')])

def pie_chart(var): 
        fig = px.pie(df, values=var, names='dep', title='Pie Chart')
        fig.show()   
        return fig
 #################################################################################################   
@app.callback(
    Output(component_id='graph', component_property='figure'),
   [Input( component_id='dep',component_property='value')])

def trace_by_dep (dep) : 
            if dep == '75':
                fig={
            'data': [
                #dep_name = df.loc[df['dep'] == dep],
                go.Line(
                   x=df.loc[df['dep'] == '75'].index,  
                   y=df.loc[df['dep'] == '75']['dc']
                )],
            'layout': go.Layout(
                title = 'Nombre de décès en Ile de France',
                xaxis = {'title': 'Days'},
                yaxis = {'title': 'Number of death'},
                hovermode='closest'
            )}
            elif dep == '59':
                fig={
            'data': [
                #dep_name = df.loc[df['dep'] == dep],
                go.Line(
                   x=df.loc[df['dep'] == '59'].index,  
                   y=df.loc[df['dep'] == '59']['dc']
                )],
            'layout': go.Layout(
                title = 'Nombre de décès dans le Nord',
                xaxis = {'title': 'Days'},
                yaxis = {'title': 'Number of death'},
                hovermode='closest'
            )} 
            elif dep == '94':
                fig={
            'data': [
                #dep_name = df.loc[df['dep'] == dep],
                go.Line(
                   x=df.loc[df['dep'] == '94'].index,  
                   y=df.loc[df['dep'] == '94']['dc']
                )],
            'layout': go.Layout(
                title = 'Nombre de décès au Val de Marne',
                xaxis = {'title': 'Days'},
                yaxis = {'title': 'Number of death'},
                hovermode='closest'
            )} 
            elif dep == '69':
                fig={
            'data': [
                #dep_name = df.loc[df['dep'] == dep],
                go.Line(
                   x=df.loc[df['dep'] == '69'].index,  
                   y=df.loc[df['dep'] == '69']['dc']
                )],
            'layout': go.Layout(
                title = 'Nombre de décès à Rhon',
                xaxis = {'title': 'Days'},
                yaxis = {'title': 'Number of death'},
                hovermode='closest'
            )} 
            elif dep == '57':
                fig={
            'data': [
                #dep_name = df.loc[df['dep'] == dep],
                go.Line(
                   x=df.loc[df['dep'] == '57'].index,  
                   y=df.loc[df['dep'] == '57']['dc']
                )],
            'layout': go.Layout(
                title = 'Nombre de décès a Moselle',
                xaxis = {'title': 'Days'},
                yaxis = {'title': 'Number of death'},
                hovermode='closest'
            )} 
     
            return fig


if __name__=='__main__': 
    app.run_server()


# In[ ]:




