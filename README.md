# p4da-capstone-api
This is Algoritma's Python for Data Analysis Capstone Project. This project aims to create a simple API to fetch data from Heroku Server. 

As a Data Scientist, we demand data to be accessible. And as a data owner, we are careful with our data. As the answer, data owner create an API for anyone who are granted access to the data to collect them. In this capstone project, we will create Flask Application as an API and deploy it to Heroku Web Hosting. 
 
___
## Dependencies : 
- Pandas    (pip install pandas)
- Flask     (pip install flask)
- Gunicorn  (pip install gunicorn)
___
## Goal 
- Create Flask API App
- Deploy to Heroku
- Build API Documentation of how your API works
- Implements the data analysis and wrangling behind the works

___
We have deployed a simple example on : https://capstone-algoritma.herokuapp.com

Here's the list of its endpoints: 
```    
1. / , method = GET
```
Base Endpoint, returning *welcoming string* value. 


```
2. /capstone/get/<data_name>/rawdata , method = GET
```
Return data **<data_name>** in JSON format. Currently available data are:
- `chinook.db`

The data that can be shown from this link is only part of the `chinook.db` data, which is a combination of **genres**, **tracks**, **media_types**, **invoice_items**, **invoices**, and **customers** dataframe. 


```
3. /capstone/get/<data_name>/rawdata/<column_name>/<value> , method = GET
```
Return all **<data_name>** (combination of genres, tracks, media_types, invoice_items, invoices, and customers dataframe) in JSON format, where the value of column **<column_name>** is equal to **<**value**>**. To check the value of **<column_name>** and **<**value**>** that can be used, open the `capstone.ipynb` on your jupyter notebook, visual studio code, or any other IDEs, and try to run the code.

Here is an example for the value that you can use :
- **<column_name>** : select one of this names [*'GenreName'*, *'GenreId'*, *'TrackName'*, *'AlbumId'*, *'MediaTypeId'*, *'Composer'*, *'Milliseconds'*, *'Bytes'*, *'MediaTypeName'*, *'InvoiceLineId'*, *'InvoiceId'*, *'TrackId'*, *'UnitPrice'*, *'Quantity'*, *'InvoiceDate'*, *'BillingAddress'*, *'BillingCity'*, *'BillingState'*, *'BillingCountry'*, *'BillingPostalCode'*, *'Total'*, *'CustomerId'*, *'FirstName'*, *'LastName'*, *'Company'*, *'Address'*, *'City'*, *'State'*, *'Country'*, *'PostalCode'*, *'Phone'*, *'Fax'*, *'Email'*, *'SupportRepId'*]

- **<**value**>** : if you select *'Company'* as your **<column_name>**, the value of <value> that you can use is one of this values [*'Microsoft Corporation'*, *'Woodstock Discos'*, *'Banco do Brasil S.A.'*, *'Apple Inc.'*, *'Riotur'*, *'Rogers Canada'*, *'JetBrains s.r.o.'*, *'Google Inc.'*, *'Telus'*, *'Embraer - Empresa Brasileira de Aeronáutica S.A.'*]


```
4. /capstone/get/<data_name>/quantity , method = GET
```
Return **<data_name>** (combination of genres, tracks, media_types, invoice_items, invoices, and customers dataframe) in JSON format, but not all of the columns from the dataframes are shown.

The columns that are shown :

- **'GenreName'** : from the **genres** dataframe
- **'MediaTypeName'** : from the **media_types** dataframe
- **'Quantity'** : from the **invoice_items** dataframe
- **'InvoiceDate'** : from **invoice** dataframe
- **'Company'** : from **customers** dataframe
- **'City'** : from **customers** dataframe
- **'Country'** : from **customers** dataframe
- **'InvoiceDay'** : from extracting the name of day in *'InvoiceDate'*
- **'InvoiceMonth'** : from extracting the month in *'InvoiceDate'*
- **'InvoiceYearMonth'** : from extracting the year and month in *'InvoiceDate'*


```
5. /capstone/get/<data_name>/quantity/prop/<index>/<columns> , method = GET
```
Return a **proportional dataframe** in JSON format, where the data is processed from the endpoint #4 dataframe. The values in the **proportional dataframe** are sums of the *'Quantity'* and then proportionated based on the value of **<**index**>** and **<**columns**>**. You can select two (2) of the values below as the combination of **<**index**>** and **<**columns**>** value :

- **'GenreName'** : from the **genres** dataframe
- **'MediaTypeName'** : from the **media_types** dataframe
- **'Company'** : from **customers** dataframe
- **'City'** : from **customers** dataframe
- **'Country'** : from **customers** dataframe
- **'InvoiceDay'** : from extracting the name of day in *'InvoiceDate'* from **invoice** dataframe
- **'InvoiceMonth'** : from extracting the month in *'InvoiceDate'* from **invoice** dataframe
- **'InvoiceYearMonth'** : from extracting the year and month in *'InvoiceDate'* from **invoice** dataframe


---

If you want to try it, you can access (copy-paste it) : 
- https://capstone-algoritma.herokuapp.com/
- https://capstone-algoritma.herokuapp.com/capstone/get/chinook.db/rawdata
- https://capstone-algoritma.herokuapp.com/capstone/get/chinook.db/rawdata/PostalCode/12227-000
- https://capstone-algoritma.herokuapp.com/capstone/get/chinook.db/quantity
- https://capstone-algoritma.herokuapp.com/capstone/get/chinook.db/quantity/prop/InvoiceMonth/GenreName
- and so on, just follow the endpoint's pattern