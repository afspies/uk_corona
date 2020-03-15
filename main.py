from src.loader import Loader
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DayLocator, DateFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.style.use('ggplot')

# Params - Taken from https://medium.com/@tomaspueyo/coronavirus-act-today-or-people-will-die-f4d3d9cd99ca
doubling_rate = 6.2  # Time it takes for number of cases to double
fatality_rate = 0.01 # Fatality rate
time_to_death = 17.3 # days from catching to dying

def main():
    l = Loader()    
    plot_data(l.data, estimate=True)

def estimate_true_cases(data):
    deaths = data[['DateVal','TotalUKDeaths']].copy()
    # TODO Sort out the cumulative nature of death data
    # deaths['DateVal'] += pd.DateOffset(-int(time_to_death))
    deaths['TotalUKDeaths'] = deaths['TotalUKDeaths'] / fatality_rate
    deaths['TotalUKDeaths'] = deaths['TotalUKDeaths'] * 2**(int(time_to_death/doubling_rate))
    return deaths

def plot_data(data:pd.DataFrame, estimate=True):
    f, ax = plt.subplots(1,1,figsize=(10,5))

    dates = data['DateVal']
    ax.bar(dates, data['CumCases'], color='c', alpha=0.6, label="Confirmed Cases")
    ax.bar(dates, data['TotalUKDeaths'], color='k', alpha=0.6, label="Deaths")

    if estimate: # Get True Number of cases estimate
        true_cases = estimate_true_cases(data)
        ax.bar(dates, true_cases['TotalUKDeaths'], color='m', alpha=0.6, label="Est. True Cases")

    months = MonthLocator(range(1, 13), bymonthday=1, interval=1)
    days = DayLocator(bymonthday=range(0,30,3))
    daysFmt = DateFormatter("%d")
    monthsFmt = DateFormatter("%b %d")

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    ax.xaxis.set_minor_locator(days)
    ax.xaxis.set_minor_formatter(daysFmt)
    
    plt.sca(ax)
    plt.xticks(rotation=60)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()