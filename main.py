from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as gr
from datetime import date
import yfinance as yfe
import streamlit as stl
import pyodbc
import pandas as pd

# creating date from which we want to get dataset
starting_date = "2017-01-01"
today_date = date.today().strftime("%Y-%m-%d")

# creating title for our web
stl.title("Stocks Market Prediction")

# creating variable to hold names of chosen company's
stocks_names = ("RIOT", "INTC.NE","FDX","UPS")

# creating selectbox with selected company's
chosen_stock = stl.selectbox("Chosen dataset for prediction", stocks_names)

# crating checkboxes if need to save to database
checkbox = stl.checkbox("Write to Database new datasets", value=True)
checkbox2 = stl.checkbox("Write to Database new predictions", value=True)

# creating connection to database
conn = pyodbc.connect('Driver={SQL Server};''Server=localhost\SQLEXPRESS;''Database=Stocks;''Trusted_Connection=True;')
cursor = conn.cursor()

# writing datasets to database

if checkbox:
    if chosen_stock == 'RIOT':
        data3 = yfe.download("RIOT", starting_date, today_date)
        data3.reset_index(inplace=True)
        stmt = 'TRUNCATE TABLE PricesRiot'
        cursor.execute(stmt)
        conn.commit()
        for index, row in data3.iterrows():
            x = ("RIOT", row['Date'], row['Open'], row['High'], row['Low'], row['Close'])
            stmt = 'INSERT INTO PricesRiot (CompanyName, PriceDate, OpenPrice, HighPrice, LowPrice, ClosePrice) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt, x)
            conn.commit()
    elif chosen_stock == 'INTC.NE':
        stmt = 'TRUNCATE TABLE PricesIntel'
        cursor.execute(stmt)
        data2 = yfe.download("INTC.NE", starting_date, today_date)
        data2.reset_index(inplace=True)
        for index, row in data2.iterrows():
            x = ("INTC.NE", row['Date'], row['Open'], row['High'], row['Low'], row['Close'])
            stmt = 'INSERT INTO PricesIntel (CompanyName, PriceDate, OpenPrice, HighPrice, LowPrice, ClosePrice) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt, x)
            conn.commit()
    elif chosen_stock == 'FDX':
        stmt = 'TRUNCATE TABLE PricesFDX'
        cursor.execute(stmt)
        data4 = yfe.download("FDX", starting_date, today_date)
        data4.reset_index(inplace=True)
        for index, row in data4.iterrows():
            x = ("FDX", row['Date'], row['Open'], row['High'], row['Low'], row['Close'])
            stmt = 'INSERT INTO PricesFDX (CompanyName, PriceDate, OpenPrice, HighPrice, LowPrice, ClosePrice) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt, x)
            conn.commit()
    elif chosen_stock == 'UPS':
        stmt = 'TRUNCATE TABLE PricesUPS'
        cursor.execute(stmt)
        data5 = yfe.download("UPS", starting_date, today_date)
        data5.reset_index(inplace=True)
        for index, row in data5.iterrows():
            x = ("UPS", row['Date'], row['Open'], row['High'], row['Low'], row['Close'])
            stmt = 'INSERT INTO PricesUPS (CompanyName, PriceDate, OpenPrice, HighPrice, LowPrice, ClosePrice) VALUES (?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt, x)
            conn.commit()

# create slider for years predictions
number_of_years = stl.slider("Years to predict", 1, 5)

period = number_of_years * 365


# create function to load data from yahoo and store in cache if want to change behavioral of app

def loading_data(stock):
    data1 = yfe.download(stock, starting_date, today_date)
    data1.reset_index(inplace=True)
    return data1


# create function to read data from database

def loading_data_db(stock):
    if chosen_stock == 'RIOT':
        stmt = "SELECT PriceDate,OpenPrice,HighPrice,LowPrice,ClosePrice FROM dbo.PricesRiot WHERE PricesRiot.CompanyName='" + stock + "'"
        data4 = pd.read_sql(stmt, conn)
        return data4
    elif chosen_stock == 'INTC.NE':
        stmt = "SELECT PriceDate,OpenPrice,HighPrice,LowPrice,ClosePrice FROM dbo.PricesIntel WHERE PricesIntel.CompanyName='" + stock + "'"
        data4 = pd.read_sql(stmt, conn)
        return data4
    elif chosen_stock == 'FDX':
        stmt = "SELECT PriceDate,OpenPrice,HighPrice,LowPrice,ClosePrice FROM dbo.PricesFDX WHERE PricesFDX.CompanyName='" + stock + "'"
        data6 = pd.read_sql(stmt, conn)
        return data6
    elif chosen_stock == 'UPS':
        stmt = "SELECT PriceDate,OpenPrice,HighPrice,LowPrice,ClosePrice FROM dbo.PricesUPS WHERE PricesUPS.CompanyName='" + stock + "'"
        data6 = pd.read_sql(stmt, conn)
        return data6


# loading data from DB
data = loading_data_db(chosen_stock)

# adding raw data to web
stl.subheader("Loaded raw data")
stl.write(data.tail())


# define function to plot raw data


def plot_chosen_data():
    figure = gr.Figure()
    figure.add_trace(gr.Scatter(x=data['PriceDate'], y=data['ClosePrice'], name='Stock Close'))
    figure.layout.update(title_text='Stocks Time frame', plot_bgcolor="white", xaxis_rangeslider_visible=True)
    stl.plotly_chart(figure)


plot_chosen_data()

# preparing data for training model
data_train = data[['PriceDate', 'ClosePrice']]
data_train = data_train.rename(columns={'PriceDate': 'ds', 'ClosePrice': 'y'})

# training model
model = Prophet()
model.fit(data_train)
future_predict = model.make_future_dataframe(periods=period)
result = model.predict(future_predict)

# writing result predictions to database

if checkbox2:
    if chosen_stock == 'RIOT':
        stmt = 'TRUNCATE TABLE PredictionsRiot'
        cursor.execute(stmt)
        conn.commit()
        for index, row in result.iterrows():
            x2 = (chosen_stock, row['ds'], row['trend'], row['yhat_lower'], row['yhat_upper'], row['trend_lower'],
                  row['trend_upper'], row['additive_terms'], row['additive_terms_lower'], row['additive_terms_upper'],
                  row['weekly'], row['weekly_lower'], row['weekly_upper'], row[result.columns.tolist()[13]],
                  row[result.columns.tolist()[14]], row[result.columns.tolist()[15]], row['multiplicative_terms'],
                  row['multiplicative_terms_lower'], row['multiplicative_terms_upper'], row['yhat'])
            stmt2 = 'INSERT INTO PredictionsRiot (CompanyName,ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt2, x2)
            conn.commit()
    elif chosen_stock == 'INTC.NE':
        stmt = 'TRUNCATE TABLE PredictionsIntel'
        cursor.execute(stmt)
        conn.commit()
        for index, row in result.iterrows():
            x3 = (chosen_stock, row['ds'], row['trend'], row['yhat_lower'], row['yhat_upper'], row['trend_lower'],
                  row['trend_upper'], row['additive_terms'], row['additive_terms_lower'], row['additive_terms_upper'],
                  row['weekly'], row['weekly_lower'], row['weekly_upper'], row[result.columns.tolist()[13]],
                  row[result.columns.tolist()[14]], row[result.columns.tolist()[15]], row['multiplicative_terms'],
                  row['multiplicative_terms_lower'], row['multiplicative_terms_upper'], row['yhat'])
            stmt3 = 'INSERT INTO PredictionsIntel (CompanyName,ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt3, x3)
            conn.commit()
    elif chosen_stock == 'FDX':
        stmt = 'TRUNCATE TABLE PredictionsFDX'
        cursor.execute(stmt)
        conn.commit()
        for index, row in result.iterrows():
            x4 = (chosen_stock, row['ds'], row['trend'], row['yhat_lower'], row['yhat_upper'], row['trend_lower'],
                  row['trend_upper'], row['additive_terms'], row['additive_terms_lower'], row['additive_terms_upper'],
                  row['weekly'], row['weekly_lower'], row['weekly_upper'], row[result.columns.tolist()[13]],
                  row[result.columns.tolist()[14]], row[result.columns.tolist()[15]], row['multiplicative_terms'],
                  row['multiplicative_terms_lower'], row['multiplicative_terms_upper'], row['yhat'])
            stmt4 = 'INSERT INTO PredictionsFDX (CompanyName,ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt4, x4)
            conn.commit()
    elif chosen_stock == 'UPS':
        stmt = 'TRUNCATE TABLE PredictionsUPS'
        cursor.execute(stmt)
        conn.commit()
        for index, row in result.iterrows():
            x5 = (chosen_stock, row['ds'], row['trend'], row['yhat_lower'], row['yhat_upper'], row['trend_lower'],
                  row['trend_upper'], row['additive_terms'], row['additive_terms_lower'], row['additive_terms_upper'],
                  row['weekly'], row['weekly_lower'], row['weekly_upper'], row[result.columns.tolist()[13]],
                  row[result.columns.tolist()[14]], row[result.columns.tolist()[15]], row['multiplicative_terms'],
                  row['multiplicative_terms_lower'], row['multiplicative_terms_upper'], row['yhat'])
            stmt5 = 'INSERT INTO PredictionsUPS (CompanyName,ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cursor.execute(stmt5, x5)
            conn.commit()


# loading result predictions from database
def loading_data_prdict_db(stock):
    if chosen_stock == 'RIOT':
        stmt = "SELECT ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat FROM dbo.PredictionsRiot WHERE PredictionsRiot.CompanyName='" + stock + "'"
        data4 = pd.read_sql(stmt, conn)
        return data4
    elif chosen_stock == 'INTC.NE':
        stmt = "SELECT ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat FROM dbo.PredictionsIntel WHERE PredictionsIntel.CompanyName='" + stock + "'"
        data4 = pd.read_sql(stmt, conn)
        return data4
    elif chosen_stock == 'FDX':
        stmt = "SELECT ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat FROM dbo.PredictionsFDX WHERE PredictionsFDX.CompanyName='" + stock + "'"
        data6 = pd.read_sql(stmt, conn)
        return data6
    elif chosen_stock == 'UPS':
        stmt = "SELECT ds,trend,yhat_lower,yhat_upper,trend_lower,trend_upper,additive_terms,additive_terms_lower,additive_terms_upper,weekly,weekly_lower,weekly_upper,yearly,yearly_lower,yearly_upper,multiplicative_terms,multiplicative_terms_lower,multiplicative_terms_upper,yhat FROM dbo.PredictionsUPS WHERE PredictionsUPS.CompanyName='" + stock + "'"
        data6 = pd.read_sql(stmt, conn)
        return data6


data_predict = loading_data_prdict_db(chosen_stock)

# displaying prediction data on web
stl.subheader("Predicted data")
stl.write(data_predict.tail())

# plotting prediction
stl.write('Prediction results')
figure1 = plot_plotly(model, data_predict)
figure1.update_layout(plot_bgcolor="white")
stl.plotly_chart(figure1)

# plotting prediction components
stl.write('Predictions components')
figure2 = model.plot_components(data_predict)
stl.write(figure2)
