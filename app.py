from flask import Flask, request 
import pandas as pd 
import sqlite3

app = Flask(__name__) 

# mendapatkan keseluruhan data dari <data_name>
@app.route('/capstone/get/<data_name>/rawdata', methods=['GET']) 
def get_data_raw(data_name): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, genres.GenreId, tracks.Name as TrackName, tracks.AlbumId, tracks.MediaTypeId, tracks.Composer, tracks.Milliseconds, tracks.Bytes, invoice_items.*, invoices.InvoiceDate, invoices.BillingAddress, invoices.BillingCity, invoices.BillingState, invoices.BillingCountry, invoices.BillingPostalCode, invoices.Total, customers.*
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn, parse_dates='InvoiceDate')

    return (x.to_json())



@app.route('/capstone/get/<data_name>/rawdata/<column_name>/<value>', methods=['GET']) 
def get_data_search(data_name, column_name, value): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, genres.GenreId, tracks.Name as TrackName, tracks.AlbumId, tracks.MediaTypeId, tracks.Composer, tracks.Milliseconds, tracks.Bytes, invoice_items.*, invoices.InvoiceDate, invoices.BillingAddress, invoices.BillingCity, invoices.BillingState, invoices.BillingCountry, invoices.BillingPostalCode, invoices.Total, customers.*
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn, parse_dates='InvoiceDate')
    x = x.astype("str")

    mask = x[column_name] == value
    x = x[mask]

    return (x.to_json())



# mendapatkan data dengan filter nilai <value> pada kolom <column>
@app.route('/capstone/get/<data_name>/quantity', methods=['GET']) 
def get_data_quantity(data_name): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, invoice_items.Quantity, customers.Country
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn)

    return (x.to_json())


@app.route('/capstone/get/<data_name>/quantity/prop', methods=['GET']) 
def get_data_prop(data_name): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, invoice_items.Quantity, customers.Country
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn)
    y = (pd.crosstab(index=x["Country"],
                    columns=x["GenreName"], 
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


@app.route('/capstone/get/<data_name>/quantity/prop/<genre_name>', methods=['GET']) 
def get_data_prop_genre(data_name, genre_name): 
    conn = sqlite3.connect("data_input/" + str(data_name))
    query = """
    SELECT genres.Name as GenreName, invoice_items.Quantity, customers.Country
    FROM genres
    JOIN tracks ON genres.GenreId == tracks.GenreId
    JOIN invoice_items ON tracks.TrackId == invoice_items.TrackId
    JOIN invoices ON invoice_items.InvoiceId == invoices.InvoiceId
    JOIN customers ON invoices.CustomerId == customers.CustomerId
    """

    x = pd.read_sql_query(query, conn)
    y = (pd.crosstab(index=x["Country"],
                    columns=x["GenreName"], 
                    values=x["Quantity"], 
                    aggfunc="sum", 
                    normalize="all", 
                    margins=True)
                    *100).\
        round(2).\
        sort_values(by="All", ascending=False, axis=1).\
        sort_values(by="All", ascending=False, axis=0).\
        astype("str")+"%"
    z = y[[str(genre_name)]]

    return (z.to_json())


if __name__ == '__main__':
    app.run(debug=True, port=5000) 