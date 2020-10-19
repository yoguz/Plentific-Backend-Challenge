# Plentific-Backend-Challenge
 Both backend and frontend codes for my 2020 application to Plentific backend job.
 
 How to Use:
 
 API URL: https://hidden-ravine-42467.herokuapp.com/api
 
 There are 4 API's to use:
 
1. /get_postcodes
 
   This API is a HTTP GET request. It provides postcodes for both chart's later querying in a JSON array format. There are currently 2391 postcodes in the DB. The result format looks like :
   
   ["AL1 ", "AL10 ", "AL2 ", "AL3 ", "AL4 ", "AL5 ", "AL6 ", "AL7 ", "AL8 ", "AL9 ", "B1 ", "B10 ", "B11 ", "B12 ", "B13 ", "B14 ".. ]
   
2. /get_dates
 
   This API is a HTTP GET request. It provides dates for both chart's later querying in a JSON array format. There are currently 308 dates(different months) in the DB. The result format looks like :
   
   ["Jan 1995", "Feb 1995", "Mar 1995", "Apr 1995", "May 1995", "Jun 1995".. ]
   
3. /get_avg_prices
 
   This API is a HTTP POST request. It provides data for chart 1 in the Backend Code Challenge. The body in request must look like:
   
    {
     "postcode":"AL1 ",
     "date_from":"Aug 2008",
     "date_to":"Aug 2009"
    }
   
   After calling the API, the result format looks like below. It provides information about average prices for the given postcode and between
the given from and to dates, separated by flats(f_avg), terraced homes(t_avg), detached homes(d_avg) and semi-detached homes(s_avg).

     [
       {
           "Date": "Aug 2008",
           "d_avg": 680833,
           "s_avg": 375745,
           "t_avg": 304970,
           "f_avg": 207293
       } ....
     ]
    
    Warning about this API: The Heroku server is not very fast and querying for this API can be slow. Not more than 2 year gap is recommended for querying for any postcode.
  
 4. /get_transaction_counts
  
    This API is a HTTP POST request. It provides data for chart 2 in the Backend Code Challenge. The body in request must look like:
    
     {
      "postcode":"OL5 ",
      "date":"Jul 2018"
     }
     
    After calling the API, the result format looks like below. It provides number of transactions in different postcodes and dates. Labels are chart labels and values are the number of transaction of each brackets. The bracket count is fixed to 8.
    
     {
       "labels": [
           "Under £184k",
           "£184k - £338k",
           "£338k - £492k",
           "£492k - £647k",
           "£647k - £801k",
           "£801k - £955k",
           "£955k - £1109k",
           "Over £1109k"
       ],
       "values": [3, 16, 20, 11, 11, 3, 1, 7]
     }

    
    
    
     
