# FSND Log Analysis Project
## Overview
**This program answers the following questions:**
1. *What are the most popular three articles of all time?*
2. *Who are the moste popular article authors of all time?*
3. *On which days did more that 1% of requests lead to errors?*

## Database Views required for this program
1. `articles_v` : 
```
create view articles_v as 
    select author, title, slug, date(time) 
    from articles;
```
2. `log_v`
```
create view log_v as 
    select substring(path, length('/articles/'), 
        length(path)) as article, 
        status, 
        date(time) as date 
    from log;
```
3. `requests_v`
```
create view requests_v as 
    select date, count(date) as number_of_requests 
    from log_v 
    group by date;
```
4. `bad_requests_v`
```
create view bad_requests_v as 
    select date, count(date) as number_of_bad_requests 
    from log_v 
    where status != '200 OK' 
    group by date;
```

## Requirements
1. python3
2. pyscopg2
3. `news` database
4. All the views mentioned above.

## Setup
To run this program:
1. Create all the views mentioned above by executing sql queries.
2. Run the script **logs_analysis.py**
```
$python3 logs_analysis.py
```

## Output
This program produces the following output:
```
---------- Most popular articles of all time ----------
Candidate is jerk, alleges rival    :     338647 views
Bears love berries, alleges bear    :     253801 views
Bad things gone, say good people    :     170098 views


----------- Most popular authors of all time ----------
Ursula La Multa                     :     507594 views
Rudolf von Treppenwitz              :     423457 views
Anonymous Contributor               :     170098 views
Markoff Chaney                      :      84557 views


------- Days with more than 1% error in requests ------
2016-07-17                          :       2.26% error
```

