from urllib.request import Request, urlopen
import datetime
from bs4 import BeautifulSoup as bs
import pandas as pd

exchange_filter = [
    'Sydney Stock Exchange',
    'Tokyo Stock Exchange',
    'Hong Kong Stock Exchange',
    'New York Stock Exchange',
    'Frankfurt Stock Exchange',
    'London Stock Exchange'
    ]

def scraper(month):
    url = 'https://www.investing.com/holiday-calendar/'
    req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
    
    webpage = urlopen(req).read()
    soup = bs(webpage, "html.parser")
    
    div_holiday = soup.find('div', id = 'holiday_div')
    navigation = div_holiday.find('table', class_ = 'genTbl closedTbl holCalTbl persistArea')
    
    try:
        holiday_data = []

        header_date = soup.find('th', class_ = 'date').text
        header_country = soup.find('th', class_ = 'country text_align_lang_base_1').text
        header_exchange = soup.find('th', class_ = 'name text_align_lang_base_1').text
        header_holiday = soup.find('th', class_ = 'holiday last text_align_lang_base_1').text
        
        for data in navigation.find_all('tr'):
            if data.find('td', class_ = 'date bold center') is not None:
                if data.find('td', class_ = 'date bold center').text != '':
                    curr_date = date = data.find('td', class_ = 'date bold center').text
                else:
                    date = curr_date
                country = data.find('td', class_= 'bold cur').text
                exchange = data.find('td', class_=None).text
                holiday = data.find('td', class_= 'last').text
                
                if month in date:
                    date = datetime.datetime.strptime(date, "%b %d, %Y")
                    date = date.strftime('%d.%m.%Y')
                    holiday_data.append([date, country, exchange, holiday])
        
        dataframe = pd.DataFrame(holiday_data, columns = [header_date, header_country, header_exchange, header_holiday] )
        
    except:
        print ('did nothing')
    
    return dataframe

def main(month):
    filepath = 'data/{}_calendar.csv'.format(month)
    
    calendar = scraper(month)
    calendar[calendar['Exchange Name'].isin(exchange_filter)].to_csv(filepath)
    print ('data/{}_calendar.csv saved'.format(month))
    
if __name__ == '__main__':
    main('Apr')