PORTFOLIO_STOCK_SHARES = '''
select mfsi.stock_name as "Stock Name", sum(mfsi.holdings_percent * mf.amount * mfasset.percentage) as "Share"
from portfolio_mutualfund mf
       inner join mutualFund_mutualfundequityallocation mfsi on mf.mutual_fund_global_id = mfsi.mutual_fund_id
       inner join mutualFund_mutualfundassetallocation mfasset
         on (mfasset.mutual_fund_id = mf.mutual_fund_global_id and mfasset.asset_class = 'Equity')
WHERE mf.created_by_id = %s
group by mfsi.stock_name
order by 2 desc
'''

PORTFOLIO_SECTOR_SHARES = '''
select mfsi.sector as "Sector", sum(mfsi.holdings_percent * mf.amount * mfasset.percentage) as "Share"
from portfolio_mutualfund mf
       inner join mutualFund_mutualfundequityallocation mfsi on mf.mutual_fund_global_id = mfsi.mutual_fund_id
    inner join mutualFund_mutualfundassetallocation mfasset on (mfasset.mutual_fund_id = mf.mutual_fund_global_id and mfasset.asset_class = 'Equity')
WHERE mf.created_by_id = %s
group by mfsi.sector
order by 2 desc
'''

PORTFOLIO_POPULAR_STOCKS = '''
select mfsi.stock_name as "Stock Name", avg(mfsi.holdings_percent) * count(*) * 100 as popularity
from portfolio_mutualfund mf
       inner join mutualFund_mutualfundequityallocation mfsi on mf.mutual_fund_global_id = mfsi.mutual_fund_id
WHERE mf.created_by_id = %s
group by mfsi.stock_name
having count(*) > 3
order by 2 desc
limit 20
'''