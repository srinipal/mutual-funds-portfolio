from django.db import connection
from .raw_sqls import PORTFOLIO_STOCK_SHARES, PORTFOLIO_SECTOR_SHARES, PORTFOLIO_POPULAR_STOCKS, \
    SIP_STOCK_SHARES, SIP_SECTOR_SHARES, SIP_POPULAR_STOCKS

OTHERS_PIE_NAME = 'Others'


def get_portfolio_stock_shares(user_id):
    stock_shares = []
    with connection.cursor() as cursor:
        cursor.execute(PORTFOLIO_STOCK_SHARES, user_id)

        for row in cursor:
            stock_shares.append({'x': row[0], 'y': row[1]})

    return stock_shares


def get_portfolio_sector_shares(user_id):
    sector_shares = []
    with connection.cursor() as cursor:
        cursor.execute(PORTFOLIO_SECTOR_SHARES, user_id)

        for row in cursor:
            sector_shares.append({'x': row[0], 'y': row[1]})

    return sector_shares


def get_portfolio_popular_stocks(user_id):
    popular_stock_shares = []
    with connection.cursor() as cursor:
        cursor.execute(PORTFOLIO_POPULAR_STOCKS, user_id)

        for row in cursor:
            popular_stock_shares.append({'x': row[0], 'y': row[1]})

    return popular_stock_shares


def get_sip_stock_shares(user_id):
    stock_shares = []
    with connection.cursor() as cursor:
        cursor.execute(SIP_STOCK_SHARES, user_id)

        for row in cursor:
            stock_shares.append({'x': row[0], 'y': row[1]})

    return stock_shares


def get_sip_sector_shares(user_id):
    sector_shares = []
    with connection.cursor() as cursor:
        cursor.execute(SIP_SECTOR_SHARES, user_id)

        for row in cursor:
            sector_shares.append({'x': row[0], 'y': row[1]})

    return sector_shares


def get_sip_popular_stocks(user_id):
    popular_stock_shares = []
    with connection.cursor() as cursor:
        cursor.execute(SIP_POPULAR_STOCKS, user_id)

        for row in cursor:
            popular_stock_shares.append({'x': row[0], 'y': row[1]})

    return popular_stock_shares


def to_2d_chart_data(stock_shares, max_categories=None):
    chart_data_set = []
    i = 0

    others_category_val = 0

    for stock_share in stock_shares:
        if max_categories is not None and i >= max_categories:
            others_category_val += int(stock_share['y'])
            continue
        chart_data_set.append({'name': stock_share['x'], 'y': int(stock_share['y'])})
        i += 1

    if others_category_val > 0:
        chart_data_set.append({'name': OTHERS_PIE_NAME, 'y': others_category_val})

    return chart_data_set


