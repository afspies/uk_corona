from urllib.request import urlretrieve
import pandas as pd
import pickle 

confirmed_case_url = "https://www.arcgis.com/sharing/rest/content/items/e5fd11150d274bebaaf8fe2a7a2bda11/data"
daily_indicators_url = "https://www.arcgis.com/sharing/rest/content/items/bc8ee90225644ef7a6f4dd1b13ea1d67/data"
data_path = "./data/"

class Loader:
    def __init__(self):
        self.update()

    def get_data(self):
        return self.data

    def load(self):
        try:
            self.data = pd.read_pickle(data_path + 'data.pkl')
        except FileNotFoundError:
            self.download(init=True)

    def save(self):
        self.data.to_pickle(data_path + 'data.pkl')

    def download(self, init=False):
        conf_cases = urlretrieve(confirmed_case_url, data_path + "DailyConfirmedCases.xlsx")
        self.conf_cases = pd.read_excel(data_path + "DailyConfirmedCases.xlsx", sep=';')
        
        if init:
            self.data = self.conf_cases
            self.save()
            return

        self.daily_ind = pd.read_excel(data_path + "DailyIndicators.xlsx", sep=';')
        daily_ind = urlretrieve(daily_indicators_url, data_path + "DailyIndicators.xlsx")
    
    def update(self):
        if not hasattr(self, 'data'):
            self.load()
    
        self.download()
    
        self.daily_ind['DateVal'] += pd.DateOffset(0)

        if len(self.data.columns) == 3:
            self.data = self.data.merge(self.daily_ind, how='outer', on='DateVal')
        else:
            self.data = self.data.merge(self.daily_ind, how='outer',
                left_on=['DateVal','TotalUKDeaths','EnglandCases','ScotlandCases','WalesCases','NICases'],
                right_on=['DateVal','TotalUKDeaths','EnglandCases','ScotlandCases','WalesCases','NICases']
                )#,)#, )
        # merge_mode = 'outer' if  else 'left'
        self.data = self.data.drop(columns=['TotalUKCases', 'NewUKCases'])
        
        self.save()

    def __str__(self):
        return self.data.to_string()
