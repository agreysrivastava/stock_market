import pandas as pd
from datetime import date
import os
class utils:
    @staticmethod
    def done_today(given_date=str(date.today())):
        df = pd.read_csv(os.getcwd() + '/static/Final_Dataframe.csv')
        last_dates = df['Entry Date'].iloc[1171:]
        for last_date in last_dates:
            if last_date == given_date:
                print(True)
                return True
        return False