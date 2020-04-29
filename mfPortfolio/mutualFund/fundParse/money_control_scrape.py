from lxml import etree
import urllib.request, urllib.error, urllib.parse
import os
from mutualFund.utils import process_utils, common_enums


def get_table_headers(thead_elem):
    tr_list = list(thead_elem)
    # first element of tr_list
    first_tr_elem = tr_list[0]
    table_headers = [process_utils.strip_off_new_line(col.text) for col in list(first_tr_elem)]
    return table_headers


def get_stock_data(stock_tr_elem):
    stock_td_list = list(stock_tr_elem)

    if len(stock_td_list) != 12:
        # print("Didn't find 12 columns, returning None")
        return None

    name = process_utils.strip_off_new_line(stock_td_list[0].find(".//span[@class='port_right']/a").text)
    sector = process_utils.strip_off_new_line(stock_td_list[1].text)
    sector_total = process_utils.strip_off_new_line(stock_td_list[2].text)
    value = process_utils.strip_off_new_line(stock_td_list[3].text)
    holdings_percent = process_utils.parse_percent(process_utils.strip_off_new_line(stock_td_list[4].text))
    prev_month_change_percent = process_utils.parse_percent(process_utils.strip_off_new_line(stock_td_list[5].text))
    past_year_highest_percent = process_utils.parse_percent(process_utils.strip_off_new_line(stock_td_list[6].text))
    past_year_lowest_percent = process_utils.parse_percent(process_utils.strip_off_new_line(stock_td_list[7].text))
    quantity = process_utils.parse_currency_val(process_utils.strip_off_new_line(stock_td_list[8].text))
    prev_month_change_qty = process_utils.parse_currency_val(process_utils.strip_off_new_line(stock_td_list[9].text))
    m_cap = process_utils.strip_off_new_line(stock_td_list[10].text)
    group_name = process_utils.strip_off_new_line(stock_td_list[11].text)

    return [name, sector, sector_total, value, holdings_percent, prev_month_change_percent, past_year_highest_percent, past_year_lowest_percent,
            quantity, prev_month_change_qty, m_cap, group_name]


def download_mf_data(mf_id, url):
    r = urllib.request.urlopen(url)
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    file_name = absolute_path + os.path.sep + "mf_pages" + os.path.sep + mf_id + '.html'
    with(open(file_name, 'wb')) as fd:
        fd.write(r.read())
    fd.close()

    return file_name


def get_stocks_data(mf_id, url):
    file_name = download_mf_data(mf_id, url)
    html_root = etree.parse(file_name, etree.HTMLParser())

    table = html_root.find("//table[@id='equityCompleteHoldingTable']")

    portfolio_percentages = {}

    equity_percent = html_root.find("//li[@data-tabname='equity']/a").text
    debt_percent = html_root.find("//li[@data-tabname='debt']/a").text
    other_percent = html_root.find("//li[@data-tabname='other']/a").text

    if equity_percent.startswith('Equity ('):
        equity_percent = process_utils.parse_percent(equity_percent[equity_percent.find('(') + 1:equity_percent.find(')')])
        portfolio_percentages[common_enums.AssetClass.EQUITY] = equity_percent

    if debt_percent.startswith('Debt ('):
        debt_percent = process_utils.parse_percent(debt_percent[debt_percent.find('(') + 1:debt_percent.find(')')])
        portfolio_percentages[common_enums.AssetClass.DEBT] = debt_percent

    if other_percent.startswith('Others ('):
        other_percent = process_utils.parse_percent(other_percent[other_percent.find('(') + 1:other_percent.find(')')])
        portfolio_percentages[common_enums.AssetClass.OTHERS] = other_percent

    rows = list(table)

    # 0. <thead>
    # 1. <tbody>

    table_headers = get_table_headers(rows[0])

    stock_data_list = []

    for stock_tr_elem in list(rows[1]):
        stock_data = get_stock_data(stock_tr_elem)

        if stock_data:
            stock_data_list.append(stock_data)

    return {"headers": table_headers, "stock_data_list": stock_data_list, "portfolio_percentages": portfolio_percentages}
