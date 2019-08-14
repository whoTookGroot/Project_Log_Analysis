# Intro

This is my submission for 'Project: Log Analysis'. While examining this submission, it would be greatly appreciated to leave critical feedback so as to better learn these languages and nip bad habits early on. 

This program connects to a postgresSQL DB via a Vagrant VM running Ubuntu 16.04.6 LTS. Upon running `logTools.py` the output will be in response to the following questions:
* __What are the most popular three articles of all time?__
* __Who are the most popular article authors of all time?__
* __On which days did more than 1% of requests lead to errors?__

# Run Instructions
- Download or manually create the [newsdata.sql](../blob/master/newsdata.sql) file
- Create the [views](../README#Views) listed below for the `news` db 
- Install `psycopg2` database adapter with `pip3 install psycopg2` or `pip3 install psycopg2-binary`
- Run the Program! `python3 logTool.py`


# Views
Works view:

```
create view works 
as 
    select author, title 
    from articles 
    group by author, title 
    order by author;
```    

Hits/Views view:
```
create view views 
as 
    select title, count 
    from (
        select title, slug 
        from articles 
        group by title, slug
    ) as s, 
        (
        select path, count(path) as count 
        from log 
        group by path) as z 
    where z.path like concat('%',s.slug) 
    order by count desc;
```


ErrorStats materialized view:

```
create materialized view errorStats 
as 
    select cast(b.code as double precision) / 
            (
            cast(a.code as double precision) + 
            cast(b.code as double precision)
            ) * 100 as perror, 
            a.date 
    from (
         select status, count(status) as code, to_char(time, 'FMMonth DD, YYYY') as date 
         from log 
         group by date, status
        ) as a, 
        (
        select status, count(status) as code, to_char(time, 'FMMonth DD, YYYY') as date 
         from log 
         group by date, status
        ) as b
    
    where a.date = b.date and a.status < b.status;
    ```


