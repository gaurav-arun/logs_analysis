#!/usr/bin/python3

import psycopg2

#################################################
# FSND Logs Analysis project
# author: Gaurav Arun (grathore07@gmail.com).
#################################################


def print_result(header: str, suffix: str, res: list) -> None:
    """
    Prints the items in results as a formatted string
    :param header: A line describing the result.
    :param suffix: Unit of each item in the result.
    :param res: List containing all the results.
    :return: None
    """
    print(header.center(55, '-'))
    for r in res:
        print('{:<35} : {:>10}{}'.format(str(r[0]), r[1], suffix))
    print()


def _db_query(query: str) -> list:
    """
    Queries the psql database and returns results.
    :param query: SQL query
    :return: result of query
    """
    try:
        db = psycopg2.connect('dbname=news')
        cur = db.cursor()
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        db.close()
        return res
    except Exception as err:
        print(err)


def get_popular_articles() -> None:
    """
    Queries the database for top 3 popular articles
    of all time and prints the article name and views.
    :return: None
    """
    header = ' Most popular articles of all time '
    suffix = ' views'
    query = '''
    select articles_v.title, count(articles_v.slug) as views
            from articles_v join log_v
            on articles_v.slug = log_v.article
            group by articles_v.slug, articles_v.title
            order by views desc limit 3;
    '''
    res = _db_query(query)
    if res:
        print_result(header, suffix, res)


def get_popular_authors() -> None:
    """
    Queries the database for top 3 popular authors
    of all time and prints the author name and views.
    :return: None
    """
    header = ' Most popular authors of all time '
    suffix = ' views'
    query = '''
    select name, count(name) as views
        from authors, articles_v, log_v
        where authors.id = articles_v.author
            and articles_v.slug = log_v.article
        group by(name)
        order by views desc;
    '''
    res = _db_query(query)
    if res:
        print_result(header, suffix, res)


def get_days_with_most_errors() -> None:
    """
    Queries the database for days with more than 1% errors(404 NOT FOUND)
    in requests that day and prints the date and error percentage.
    :return: None
    """
    header = ' Days with more than 1% error in requests '
    suffix = '% error'
    query = '''
    select bad_requests_v.date,
        round((100.0 * number_of_bad_requests / number_of_requests), 2)
            as error
        from requests_v join bad_requests_v
        on requests_v.date = bad_requests_v.date
        where number_of_bad_requests > 0.01 * number_of_requests;
    '''
    res = _db_query(query)
    if res:
        print_result(header, suffix, res)


if __name__ == '__main__':
    queries = [get_popular_articles, get_popular_authors, get_days_with_most_errors]
    for query in queries:
        print()
        query()
