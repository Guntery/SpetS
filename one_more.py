from spyre import server

import pandas as pd
#import urllib.request
#import urllib.error
import matplotlib.pyplot as plt
#import cherrypy

class StockExample(server.App):
  title = "Inputs"

  inputs = [{   "type":'dropdown',
                "label": 'Індекс',
                "options" : [ {"label": "VCI", "value":"VCI"},
                                {"label": "TCI", "value":"TCI"},
                                {"label": "VHI", "value":"VHI"},],
                "key": 'index',
                "action_id": "update_data"},

              { "type":'dropdown',
                "label": 'Область',
                "options" : [ {"label": "Вінниця", "value":"01"},
                                  {"label": "Волинь", "value":"02"},
                                  {"label": "Дніпро", "value":"03"},
                                  {"label": "Донецьк", "value":"04"},
                                  {"label": "Житомир", "value":"05"},
                                  {"label": "Закарпаття", "value":"06"},
                                  {"label": "Запоріжжя", "value":"07"},
                                  {"label": "Франкцівськ", "value":"08"},
                                  {"label": "Київ", "value":"09"},
                                  {"label": "Кіровоград", "value":"10"},
                                  {"label": "Луганськ", "value":"11"},
                                  {"label": "Львів", "value":"12"},
                                  {"label": "Миколаїв", "value":"13"},
                                  {"label": "Одеса", "value":"14"},
                                  {"label": "Полтава", "value":"15"},
                                  {"label": "Рівне", "value":"16"},
                                  {"label": "Суми", "value":"17"},
                                  {"label": "Терпнопіль", "value":"18"},
                                  {"label": "Харків", "value":"19"},
                                  {"label": "Херсон", "value":"20"},
                                  {"label": "Проскурів", "value":"21"},
                                  {"label": "Черкаси", "value":"22"},
                                  {"label": "Чернівці", "value":"23"},
                                  {"label": "Чернігів", "value":"24"},
                                  {"label": "АРК", "value":"25"},
                                  {"label": "Київ місто", "value":"26"},
                                  {"label": "Севастополь", "value":"27"}],
                "key": 'region',
                "action_id": "update_data"},

              { "input_type":"text",
                "variable_name":"year",
                "label": "Рік",
                "value":1981,
                "key": 'year',
                "action_id":"update_data"},

              { "type":'slider',
                "label": 'Перший тиждень',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'first',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Останній тиждень',
                "min" : 1,"max" : 52,"value" : 35,
                "key": 'last',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Відсоток площі',
                "min" : 0,"max" : 100,"value" : 0,
                "key": 'percent',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Мінімум VHI',
                "min" : 0,"max" : 100,"value" : 0,
                "key": 'minimum',
                "action_id": 'update_data'},

              { "type":'slider',
                "label": 'Максимум VHI',
                "min" : 0,"max" : 100,"value" : 100,
                "key": 'maximum',
                "action_id": 'update_data'},]

  controls = [{   "type" : "hidden",
                  "id" : "update_data"}]

  tabs = ["Графік", "Таблиця", "Посуха", "Екстремуми", "Розмір"]

  outputs = [{  "type" : "plot",
                "id" : "plot",
                "control_id" : "update_data",
                "tab" : "Графік"},
              { "type" : "table",
                "id" : "table",
                "control_id" : "update_data",
                "tab" : "Таблиця"},
              { "type" : "html",
                "id" : "drought",
                "control_id" : "update_data",
                "tab" : "Посуха"},
              { "type" : "table",
                "id" : "table1",
                "control_id" : "update_data",
                "tab" : "Екстремуми"},
              { "type" : "html",
                "id" : "data_size",
                "control_id" : "update_data",
                "tab" : "Розмір"}]

  def table(self, params):
    index = params['index']
    region = params['region']
    year = params['year']
    first = params['first']
    last = params['last']

    path = 'C:/Users/User/Desktop/cleaned/2016_04_09-11h_vhi_id_{}.csv'.format(region)

    df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
    df1 = df[(df['year'] == float(year)) & (df['week'] >= float(first)) & (df['week'] <= float(last))]
    df1 = df1[['week', index]]
    return df1

  def getPlot(self, params):
    index = params['index']
    year = params['year']
    first = params['first']
    last = params['last']
    df = self.table(params).set_index('week')
    plt_obj = df.plot()
    plt_obj.set_ylabel(index)
    plt_obj.set_title('Index {index} for {year} from {first} to {last} weeks'.format(index=index,
      year=float(year), first=float(first), last=float(last)))
    fig = plt_obj.get_figure()
    return fig

  def drought(self, params):
    region = params['region']
    minimum = params['minimum']
    maximum = params['maximum']
    percent = params['percent']

    path = 'C:/Users/User/Desktop/cleaned/2016_04_09-11h_vhi_id_{}.csv'.format(region)
    df = pd.read_csv(path, index_col=False, header=9,
                     names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
    df1 = df[(df['VHI'] < int(maximum)) & (df['VHI'] > int(minimum)) & (df['VHI<15'] > int(percent))]
    df1 = df1[['year', 'VHI', 'VHI<15']]
    return 'Роки із відсотком площі > {percent} з посухою: {years}'.format(percent=int(percent),
      years = pd.unique(df1.year.ravel()))

  def table1(self, params):
      index = params['index']
      region = params['region']
      year = params['year']

      path = 'C:/Users/User/Desktop/cleaned/2016_04_09-11h_vhi_id_{}.csv'.format(region)

      df = pd.read_csv(path, index_col=False, header=9,
                       names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])
      return df.loc[pd.concat((df.groupby(['year'])['VHI'].idxmax(), df.groupby(['year'])['VHI'].idxmin()))]

  def data_size(self, params):
      region = params['region']
      path = 'C:/Users/User/Desktop/cleaned/2016_04_09-11h_vhi_id_{}.csv'.format(region)

      df = pd.read_csv(path, index_col=False, header=9,
                       names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'])

      return 'Розмір dataframe: {size}'.format(size=df.shape)


app = StockExample()
app.launch(port=8080)
