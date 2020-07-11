import dash
import os
from dash.dependencies import Input, Output
import dash_table
import requests
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from bs4 import BeautifulSoup

link = 'https://www.mohfw.gov.in/'
req = requests.get(link)
soup = BeautifulSoup(req.content, "html.parser")
thead = soup.find_all('thead')[-1]
head = thead.find_all('tr')
tbody = soup.find_all('tbody')[0]
body = tbody.find_all('tr')
head_rows = []
body_rows = []
colors = {
    'background': '#343A40',
    'text': 'white'
}
for tr in head:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    head_rows.append(row)
for tr in body:
    td = tr.find_all(['th', 'td'])
    row = [i.text for i in td]
    body_rows.append(row)
df_bs = pd.DataFrame(data=body_rows[:len(body_rows) - 6], columns=head_rows[0])
df_bs.drop('S. No.', axis=1, inplace=True)
df_India = df_bs.copy()
df_India['Total Confirmed cases*'] = df_India['Total Confirmed cases*'].apply(lambda x: int(x))
df_India['Active Cases*'] = df_India['Active Cases*'].apply(lambda x: int(x))
df_India['Cured/Discharged/Migrated*'] = df_India['Cured/Discharged/Migrated*'].apply(lambda x: int(x))
df_India['Deaths**'] = df_India['Deaths**'].apply(lambda x: int(x))

total_confirmed_cases_high_to_low = df_India.sort_values('Total Confirmed cases*')[::-1]
total_confirmed_deaths_high_to_low = df_India.sort_values('Deaths**')[::-1]
total_confirmed_active_high_to_low = df_India.sort_values('Active Cases*')[::-1]
total_confirmed_cured_high_to_low = df_India.sort_values('Cured/Discharged/Migrated*')[::-1]

##################################Grabbing active,cured,death count#####################################################
stats = soup.find_all(class_='site-stats-count')
ul_list = stats[0].find_all('ul')[0]
strong_ls = ul_list.find_all('strong')
status = []
for i in strong_ls:
    status.append(i.text)
active = status[0]
cured = status[1]
deaths = status[2]

####################################Total confirmed cases(Bar plot)#####################################################
fig = px.bar(data_frame=total_confirmed_cases_high_to_low,
             x='Name of State / UT',
             y='Total Confirmed cases*',
             labels={'Total Confirmed cases*': 'Total Confirmed cases', 'Name of State / UT': 'State'},
             title='Confirmed cases', )
fig.update_layout(barmode='group',
                  xaxis_tickangle=-45,
                  height=700,
                  title={'y': 0.9, 'x': 0.5},
                  plot_bgcolor=colors['background'],
                  paper_bgcolor=colors['background'],
                  font_color=colors['text'])
fig.update_traces(marker_color='#636EFA',
                  marker_line_color='#636EFA')

####################################Total confirmed death cases(Bar plot)###############################################
fig_deaths = px.bar(data_frame=total_confirmed_deaths_high_to_low,
                    x='Name of State / UT',
                    y='Deaths**',
                    labels={'Name of State / UT': 'State', 'Deaths**': 'Deaths'},
                    title='Confirmed deaths', )
fig_deaths.update_layout(barmode='group',
                         xaxis_tickangle=-45,
                         height=700,
                         title={'y': 0.9, 'x': 0.5},
                         plot_bgcolor=colors['background'],
                         paper_bgcolor=colors['background'],
                         font_color=colors['text'])
fig_deaths.update_traces(marker_color='#cfff00',
                         marker_line_color='#cfff00')

##########################################Total confirmed active cases(line plot)#######################################
fig_act = px.line(data_frame=total_confirmed_active_high_to_low,
                  x='Name of State / UT',
                  y='Active Cases*',
                  labels={'Name of State / UT': 'State', 'Active Cases*': 'Active Cases'},
                  title='Confirmed Active Cases')
fig_act.update_layout(barmode='group',
                      xaxis_tickangle=-45,
                      height=600,
                      title={'y': 0.9, 'x': 0.5},
                      plot_bgcolor=colors['background'],
                      paper_bgcolor=colors['background'],
                      font_color=colors['text'],
                      xaxis=dict(showgrid=False),
                      yaxis=dict(showgrid=False))
fig_act.update_traces(line_color='#ff5722')

###############################################Total confirmed discharged cases(line plot)##############################
fig_dischar = px.line(data_frame=total_confirmed_cured_high_to_low,
                      x='Name of State / UT',
                      y='Cured/Discharged/Migrated*',
                      labels={'Name of State / UT': 'State', 'Cured/Discharged/Migrated*': 'Discharged'},
                      title='Confirmed Discharged Cases')
fig_dischar.update_layout(barmode='group',
                          xaxis_tickangle=-45,
                          height=600,
                          title={'y': 0.9, 'x': 0.5},
                          plot_bgcolor=colors['background'],
                          paper_bgcolor=colors['background'],
                          font_color=colors['text'],
                          xaxis=dict(showgrid=False),
                          yaxis=dict(showgrid=False)
                          )
fig_dischar.update_traces(line_color='#ff5722')

#########################Distribution of Total,Active,Discharge & Deceased(Stacked bar plot)############################
total_confirmed_vs_active = df_India.sort_values('Total Confirmed cases*')[::-1]
state = total_confirmed_vs_active['Name of State / UT']
ac = total_confirmed_vs_active['Active Cases*']
dc = total_confirmed_vs_active['Cured/Discharged/Migrated*']
tc = total_confirmed_vs_active['Total Confirmed cases*']
de = total_confirmed_vs_active['Deaths**']
fig_dist = go.Figure(data=[
    go.Bar(name='Deceased',
           x=state,
           y=de,
           text=de,
           textposition='auto',
           marker_color='red',
           marker_line_color='red'),
    go.Bar(name='Discharged',
           x=state,
           y=dc,
           text=dc,
           textposition='auto',
           marker_color='#fccfd4',
           marker_line_color='#fccfd4'),
    go.Bar(name='Active',
           x=state,
           y=ac,
           text=ac,
           textposition='auto',
           marker_color='#f99fa8',
           marker_line_color='#f99fa8'),
    go.Bar(name='Total confirmed',
           x=state,
           y=tc,
           text=tc,
           textposition='auto',
           marker_color='#f67280',
           marker_line_color='#f67280'),
])
fig_dist.update_layout(title_text='Distribution of Total,Active,Discharge & Deceased',
                       title={'y': 0.92, 'x': 0.5},
                       barmode='stack',
                       xaxis=dict(showgrid=False),
                       height=700,
                       yaxis=go.layout.YAxis(title='Count', showticklabels=False, showgrid=False),
                       plot_bgcolor=colors['background'],
                       paper_bgcolor=colors['background'],
                       font_color=colors['text'],
                       legend=dict(x=0.85, y=1)
                       )
fig_dist.update_traces(textposition='auto')

#########################################Total confirmed cases(Scatter plot)############################################
path = 'https://raw.githubusercontent.com/imdevskp/covid-19-india-data/master/nation_level_daily.csv'
history = pd.read_csv(path)
fig_timeseries_total = go.Figure()
fig_timeseries_total.add_trace(go.Scatter(fill='tonexty',
                                          line=dict(color='rgba(76, 30, 170,0.5)', width=3),
                                          line_color='#884dff',
                                          x=history['Date'],
                                          y=history['Total Confirmed'],
                                          mode='lines+markers',
                                          marker=dict(color='rgb(76, 30, 170)')))
fig_timeseries_total.update_layout(title_text='Total Confirmed Cases (Date basis)',
                                   title={'y': 0.9, 'x': 0.5},
                                   paper_bgcolor='rgba(76, 30, 170,0.15)',
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   font_color=colors['text'],
                                   xaxis=dict(showgrid=False),
                                   yaxis=dict(showgrid=False, side='right'),
                                   xaxis_title="Date",
                                   yaxis_title="Cases",
                                   hovermode='x unified',
                                   hoverlabel_align='auto',
                                   hoverlabel=dict(bgcolor='#383751')
                                   )
fig_timeseries_total.update_xaxes(showspikes=True,
                                  showgrid=False,
                                  showline=True,
                                  linewidth=2,
                                  linecolor='rgb(76, 30, 170)',
                                  range=[0, history['Date'].count()],
                                  showticklabels=True,
                                  ticks=('outside'),
                                  tickwidth=2,
                                  tickcolor='#4C1EAA')
fig_timeseries_total.update_yaxes(showspikes=True,
                                  showgrid=False,
                                  showline=True,
                                  linewidth=2,
                                  linecolor='rgb(76, 30, 170)',
                                  range=[0, history['Total Confirmed'].max() + 80000],
                                  showticklabels=True,
                                  ticks=('outside'),
                                  tickwidth=2,
                                  tickcolor='#4C1EAA')

#######################################Daily confirmed cases(Scatter plot)##############################################
fig_timeseries_daily = go.Figure()
fig_timeseries_daily.add_trace(go.Scatter(fill='tonexty',
                                          line=dict(color='rgba(76, 30, 170,0.5)', width=3),
                                          line_color='#c70039',
                                          x=history['Date'],
                                          y=history['Daily Confirmed'],
                                          mode='lines+markers',
                                          marker=dict(color='rgb(199, 0, 57)')))
fig_timeseries_daily.update_layout(title_text='Daily Confirmed Cases (Date basis)',
                                   title={'y': 0.9, 'x': 0.5},
                                   paper_bgcolor='rgba(199, 0, 57,0.15)',
                                   plot_bgcolor='rgba(0,0,0,0)',
                                   font_color=colors['text'],
                                   xaxis=dict(showgrid=False),
                                   yaxis=dict(showgrid=False, side='right'),
                                   xaxis_title="Date",
                                   yaxis_title="Cases",
                                   hovermode='x unified',
                                   hoverlabel_align='auto',
                                   hoverlabel=dict(bgcolor='#383751')
                                   )
fig_timeseries_daily.update_xaxes(showspikes=True,
                                  showgrid=False,
                                  showline=True,
                                  linewidth=2,
                                  linecolor='#c70039',
                                  range=[0, history['Date'].count()],
                                  showticklabels=True,
                                  ticks=('outside'),
                                  tickwidth=2,
                                  tickcolor='#4C1EAA')
fig_timeseries_daily.update_yaxes(showspikes=True,
                                  showgrid=False,
                                  showline=True,
                                  linewidth=2,
                                  linecolor='#c70039',
                                  range=[0, history['Daily Confirmed'].max()],
                                  showticklabels=True,
                                  ticks=('outside'),
                                  tickwidth=2,
                                  tickcolor='#4C1EAA')

#######################################Total vs Daily Cases(Scatter plot)###############################################
fig_daily_vs_total = go.Figure()
fig_daily_vs_total.add_trace(
    go.Line(x=history['Date'],
            y=history['Daily Confirmed'],
            fillcolor='rgba(0, 0, 0)',
            stackgroup='one',
            marker_color='black',
            name='Daily cases'))
fig_daily_vs_total.add_trace(
    go.Scatter(x=history['Date'],
               y=history['Total Confirmed'],
               fillcolor='rgba(0, 255, 97,0.6)',
               stackgroup='one',
               marker_color='#00ff61',
               name='Total cases'))
fig_daily_vs_total.update_layout(plot_bgcolor=colors['background'],
                                 paper_bgcolor=colors['background'],
                                 font_color=colors['text'],
                                 xaxis=dict(showgrid=False),
                                 yaxis=dict(showgrid=False, side='right'),
                                 title_text='Total vs Daily Cases',
                                 title={'y': 0.9, 'x': 0.5},
                                 xaxis_title="Date",
                                 yaxis_title="Count",
                                 legend=dict(x=0, y=1)
                                 )

#############################################Total vs Daily Recoverd Cases(Scatter plot)################################
fig_daily_vs_total_recv = go.Figure()
fig_daily_vs_total_recv.add_trace(
    go.Line(x=history['Date'],
            y=history['Daily Recovered'],
            fillcolor='rgba(0, 0, 0)',
            stackgroup='one',
            marker_color='black',
            name='Daily Recovered'))
fig_daily_vs_total_recv.add_trace(
    go.Scatter(x=history['Date'],
               y=history['Total Recovered'],
               fillcolor='rgba(0, 255, 97,0.6)',
               stackgroup='one',
               marker_color='#00ff61',
               name='Total Recovered'))
fig_daily_vs_total_recv.update_layout(plot_bgcolor=colors['background'],
                                      paper_bgcolor=colors['background'],
                                      font_color=colors['text'],
                                      xaxis=dict(showgrid=False, autorange='reversed'),
                                      yaxis=dict(showgrid=False),
                                      title_text='Total vs Daily Recoverd',
                                      title={'y': 0.9, 'x': 0.5},
                                      xaxis_title="Date",
                                      yaxis_title="Count",
                                      legend=dict(x=0.7, y=1),
                                      )

###############################################Total vs Daily Deceased(Scatter plot)####################################
fig_total_vs_daily_deceased = go.Figure()
fig_total_vs_daily_deceased.add_trace(go.Line(x=history['Date'],
                                              fillcolor='rgba(0, 0, 0)',
                                              y=history['Daily Deceased'],
                                              stackgroup='one',
                                              marker_color='black',
                                              name='Daily Deceased'))
fig_total_vs_daily_deceased.add_trace(go.Scatter(x=history['Date'],
                                                 y=history['Total Deceased'],
                                                 stackgroup='one',
                                                 fillcolor='rgba(0, 255, 97,0.6)',
                                                 marker_color='#00ff61',
                                                 name='Total Deceased'))
fig_total_vs_daily_deceased.update_layout(plot_bgcolor=colors['background'],
                                          paper_bgcolor=colors['background'],
                                          font_color=colors['text'],
                                          xaxis=dict(showgrid=False),
                                          yaxis=dict(showgrid=False, side='right'),
                                          title_text='Total vs Daily Deceased',
                                          title={'y': 0.9, 'x': 0.5},
                                          xaxis_title="Date",
                                          yaxis_title="Count",
                                          legend=dict(x=0, y=1)
                                          )

######################Daily Deceased,Recovered,Confirmed Cases(One line,Two Scatter plots)##############################
fig_daily_drc = go.Figure()
fig_daily_drc.add_trace(go.Line(x=history['Date'],
                                y=history['Daily Confirmed'],
                                fillcolor='rgba(243, 113, 33,0.6)',
                                stackgroup='three',
                                marker_color='#f37121',
                                name='Daily Confirmed'))
fig_daily_drc.add_trace(go.Scatter(x=history['Date'],
                                   y=history['Daily Recovered'],
                                   fillcolor='rgba(199, 0, 57,0.7)',
                                   stackgroup='two',
                                   marker_color='#c70039',
                                   name='Daily Recovered'))
fig_daily_drc.add_trace(go.Scatter(x=history['Date'],
                                   y=history['Daily Deceased'],
                                   fillcolor='rgba(17, 29, 94,0.9)',
                                   stackgroup='one',
                                   marker_color='#111d5e',
                                   name='Daily Deceased'))
fig_daily_drc.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(17, 29, 94,0.3)',
                            font_color=colors['text'],
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=False, side='right'),
                            title_text='Daily Deceased,Recovered,Confirmed',
                            title={'y': 0.9, 'x': 0.5},
                            xaxis_title="Date",
                            yaxis_title="Count",
                            legend=dict(x=0, y=1),
                            height=500),

########################Total Deceased,Recovered,Confirmed Cases(One line,Two Scatter plots)############################
fig_total_drc = go.Figure()
fig_total_drc.add_trace(go.Line(x=history['Date'],
                                y=history['Total Confirmed'],
                                fillcolor='rgba(243, 113, 33,0.6)',
                                stackgroup='three',
                                marker_color='#f37121',
                                name='Daily Confirmed'))
fig_total_drc.add_trace(go.Scatter(x=history['Date'],
                                   y=history['Total Recovered'],
                                   fillcolor='rgba(199, 0, 57,0.7)',
                                   stackgroup='two',
                                   marker_color='#c70039',
                                   name='Daily Recovered'))
fig_total_drc.add_trace(go.Scatter(x=history['Date'],
                                   y=history['Total Deceased'],
                                   fillcolor='rgba(17, 29, 94,0.9)',
                                   stackgroup='one',
                                   marker_color='#111d5e',
                                   name='Daily Deceased'))
fig_total_drc.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(17, 29, 94,0.3)',
                            font_color=colors['text'],
                            xaxis=dict(showgrid=False),
                            yaxis=dict(showgrid=False, side='right'),
                            title_text='Total Deceased,Recovered,Confirmed',
                            title={'y': 0.9, 'x': 0.5},
                            xaxis_title="Date",
                            yaxis_title="Count",
                            legend=dict(x=0, y=1),
                            height=500),

#####################################Active,Cured,Death rates(pie chart)################################################
fig_pie = go.Figure()
# pie_colors = ['#CCFF00','#0000FF','#FF0033']
active_ = int(status[0])
cured_ = int(status[1])
deaths_ = int(status[2])
labels = ['Active', 'Cured', 'Deaths']
values = [active, cured, deaths]
fig_pie.add_trace(go.Pie(labels=labels,
                         values=values,
                         textinfo='label+percent',
                         showlegend=False, ))
fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(17, 29, 94,0.3)',
                      font_color=colors['text'], )

########################################################################################################################
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                external_scripts=['https://use.fontawesome.com/949eaebb83.js'])
server = app.server
app.title = 'COVID-19'
app.layout = html.Div(className='::-webkit-scrollbar',
                      style={'backgroundColor': colors['background'], 'margin': 'auto', 'overflow': 'scroll'},
                      children=[html.Div(children=[
                          html.Div(children=[
                              dcc.Loading(type='cube'),
                              dbc.Row([dbc.Col(dcc.Markdown('# Welcome to COVID-19 dashboard\n A Project by [Preetham](https://github.com/preethampy "GitHub").',
                                                       style={'color': 'white', 'margin': 'auto',
                                                              'padding-top': '280px',
                                                              "white-space": "pre",
                                                              'font-size':'20px'}),
                                               #width={"size": 6, "offset": 3},
                                               ),
                                       ],
                                      style={'height': '100vh', 'margin': 'auto'}),
                          ],
                              style={'height': '100vh',
                                     'background': '#343A40',
                                     'font-family': 'Arial',
                                     'font-weight': 'bolder',
                                     'text-align': 'center',
                                     'vertical-align': 'middle'}),
                          html.Div(children=[dbc.Row([dbc.Col(
                              children=[html.Img(src='assets/2.png',
                                                 style={'float': 'left', 'padding': '20px'}),
                                        html.P(active,
                                               style={'font-weight': 'bold', 'font-size': '25px',
                                                      'margin-top': '16px'}),
                                        html.P('Active', style={})], md=3,
                              style={'text-align': 'right', 'background-color': '#ff631c', 'border-radius': '5px'}),
                              dbc.Col(children=[
                                  html.Img(src='assets/family.png', style={'float': 'left', 'padding': '22px'}),
                                  html.P(cured,
                                         style={'font-weight': 'bold', 'font-size': '25px', 'margin-top': '16px'}),
                                  html.P('Cured / Discharged')], md=3,
                                  style={'text-align': 'right', 'background-color': '#4d70ff', 'border-radius': '5px'}),
                              dbc.Col(children=[
                                  html.Img(src='assets/angel.png', style={'float': 'left', 'padding': '22px'}),
                                  html.P(deaths,
                                         style={'font-weight': 'bold', 'font-size': '25px', 'margin-top': '16px'}),
                                  html.P('Deaths')],
                                  md=3,
                                  style={'text-align': 'right', 'background-color': '#fa1616',
                                         'border-radius': '5px'})],
                              style={'padding-left': '100px', 'padding-right': '100px', 'padding-bottom': '50px'},
                              className='justify-content-between')],
                              style={'background': '#343A40', }),
                          dash_table.DataTable(id='table-paging-and-sorting',
                                               style_data_conditional=[
                                                   {
                                                       'if': {'row_index': 'odd'},
                                                       'backgroundColor': '#343A40',
                                                   }
                                               ],
                                               style_table={'overflowX': 'auto', 'padding-left': '19px'},
                                               style_cell_conditional=[
                                                   {
                                                       'if': {'column_id': 'Name of State / UT'},
                                                       'padding-left': '40px',
                                                   },

                                               ],
                                               style_as_list_view=True,
                                               style_data={'border': '0px solid black'},
                                               style_header={'backgroundColor': '#343A40', 'border': '0px solid black',
                                                             'font-weight': 'bold', 'font-size': '14px'},
                                               style_cell={
                                                   'backgroundColor': '#44494E',
                                                   'color': 'white',
                                                   'textAlign': 'center',
                                                   'overflowX': 'auto',
                                                   'height': '35px',
                                                   'font-size': '13px'
                                               },
                                               columns=[{'name': i, 'id': i} for i in df_India.columns],
                                               data=df_India.to_dict('records'),
                                               page_action='custom',
                                               sort_action='custom',
                                               sort_mode='single',
                                               sort_by=[], ),
                          dcc.Graph(figure=fig),
                          dcc.Graph(figure=fig_deaths),
                          dbc.Row([dbc.Col(dcc.Graph(figure=fig_act), md=6, style={'padding-bottom': '150px'}),
                                   dbc.Col(dcc.Graph(figure=fig_dischar), md=6)]),
                          dcc.Graph(figure=fig_dist),
                          dcc.Graph(figure=fig_timeseries_total),
                          dcc.Graph(figure=fig_timeseries_daily),
                          dbc.Row([dbc.Col(dcc.Graph(figure=fig_daily_vs_total), md=6, style={'padding': '0px'}),
                                   dbc.Col(dcc.Graph(figure=fig_daily_vs_total_recv), md=6, style={'padding': '0px'})]),
                          dcc.Graph(figure=fig_total_vs_daily_deceased),
                          dcc.Graph(figure=fig_daily_drc),
                          dcc.Graph(figure=fig_total_drc),
                          dcc.Graph(figure=fig_pie),
                      ])])


@app.callback(Output('table-paging-and-sorting', 'data'), [Input('table-paging-and-sorting', 'sort_by')])
def update_table(sort_by):
    if len(sort_by):
        dff = df_India.sort_values(by=sort_by[0]['column_id'], inplace=False,
                                   ascending=sort_by[0]['direction'] == 'asc')
    else:
        dff = df_India
    return dff.to_dict('records')


if __name__ == '__main__':
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
    app.run_server(debug=False)
