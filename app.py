from flask import Flask, request 
import pandas as pd 
import sqlite3


app = Flask(__name__) 


# 1. Welcoming string
@app.route('/')
def home():
    return "<h1>Hello, Welcome to Viorie's API Capstone</h1>"


# 2. Get all the data from <data_name>, but only restricted to genres, tracks, media_types, invoice_items, invoices, and customers dataframe
@app.route('/capstone/get/<data_name>/rawdata', methods=['GET']) 
def get_data_raw(data_name): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, genres.GenreId, tracks.Name as TrackName, tracks.AlbumId, tracks.MediaTypeId, tracks.Composer, tracks.Milliseconds, tracks.Bytes, media_types.Name as MediaTypeName, invoice_items.*, invoices.InvoiceDate, invoices.BillingAddress, invoices.BillingCity, invoices.BillingState, invoices.BillingCountry, invoices.BillingPostalCode, invoices.Total, customers.*
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN media_types ON tracks.MediaTypeId == media_types.MediaTypeId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn, parse_dates="InvoiceDate")

    return (x.to_json())


# 3. Search <column_name> and <value> from <data_name>, but only restricted to genres, tracks, media_types, invoice_items, invoices, and customers dataframe
@app.route('/capstone/get/<data_name>/rawdata/<column_name>/<value>', methods=['GET']) 
def get_data_search(data_name, column_name, value): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, genres.GenreId, tracks.Name as TrackName, tracks.AlbumId, tracks.MediaTypeId, tracks.Composer, tracks.Milliseconds, tracks.Bytes, media_types.Name as MediaTypeName, invoice_items.*, invoices.InvoiceDate, invoices.BillingAddress, invoices.BillingCity, invoices.BillingState, invoices.BillingCountry, invoices.BillingPostalCode, invoices.Total, customers.*
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN media_types ON tracks.MediaTypeId == media_types.MediaTypeId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn, parse_dates="InvoiceDate")
    x = x.astype("str")

    mask = x[column_name] == value
    x = x[mask]

    return (x.to_json())


# 4. Get part of the data from <data_name>, but only restricted to quantity-related data
@app.route('/capstone/get/<data_name>/quantity', methods=['GET']) 
def get_data_quantity(data_name): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, media_types.Name as MediaTypeName, invoice_items.Quantity, invoices.InvoiceDate, customers.Company, customers.City, customers.Country
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN media_types ON tracks.MediaTypeId == media_types.MediaTypeId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn, parse_dates="InvoiceDate")
    
    x["InvoiceDay"] = x["InvoiceDate"].dt.weekday_name
    x["InvoiceDay"] = pd.Categorical(x["InvoiceDay"], categories=['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'], ordered=True)

    x["InvoiceMonth"] = x["InvoiceDate"].dt.month
    x["InvoiceMonth"] = x["InvoiceMonth"].replace({
        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "November",
        12 : "December"})
    x["InvoiceMonth"] = pd.Categorical(x["InvoiceMonth"], categories=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], ordered=True)

    x["InvoiceYearMonth"] = x["InvoiceDate"].dt.to_period('M')

    return (x.to_json())


# 5. Get proportional table of quantity from <data_name> with dynamic <index> and <columns>
@app.route('/capstone/get/<data_name>/quantity/prop/<index>/<columns>', methods=['GET']) 
def get_data_prop(data_name, index, columns): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, media_types.Name as MediaTypeName, invoice_items.Quantity, invoices.InvoiceDate, customers.Company, customers.City, customers.Country
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN media_types ON tracks.MediaTypeId == media_types.MediaTypeId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn, parse_dates="InvoiceDate")
    
    x["InvoiceDay"] = x["InvoiceDate"].dt.weekday_name
    x["InvoiceDay"] = pd.Categorical(x["InvoiceDay"], categories=['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'], ordered=True)

    x["InvoiceMonth"] = x["InvoiceDate"].dt.month
    x["InvoiceMonth"] = x["InvoiceMonth"].replace({
        1 : "January",
        2 : "February",
        3 : "March",
        4 : "April",
        5 : "May",
        6 : "June",
        7 : "July",
        8 : "August",
        9 : "September",
        10 : "October",
        11 : "November",
        12 : "December"})
    x["InvoiceMonth"] = pd.Categorical(x["InvoiceMonth"], categories=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], ordered=True)

    x["InvoiceYearMonth"] = x["InvoiceDate"].dt.to_period('M')

    y = (pd.crosstab(index=x[str(index)],
                    columns=x[str(columns)], 
                    values=x["Quantity"], 
                    aggfunc="sum", 
                    normalize="all", 
                    margins=True)
                    *100).\
        round(2).\
        sort_values(by="All", ascending=False, axis=1).\
        sort_values(by="All", ascending=False, axis=0).\
        astype("str")+"%"

    return (y.to_json())


if __name__ == '__main__':
    app.run(debug=True, port=5000) 