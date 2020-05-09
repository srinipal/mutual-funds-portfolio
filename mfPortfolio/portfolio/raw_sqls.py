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

SIP_STOCK_SHARES='''
select mfsi.stock_name as "Stock Name", sum(mfsi.holdings_percent * msip.amount * mfasset.percentage) as "Share"
from portfolio_mutualfund mf
       inner join portfolio_mutualfundsip msip on mf.id = msip.mutual_fund_id
       inner join mutualFund_mutualfundequityallocation mfsi on mf.mutual_fund_global_id = mfsi.mutual_fund_id
       inner join mutualFund_mutualfundassetallocation mfasset
         on (mfasset.mutual_fund_id = mf.mutual_fund_global_id and mfasset.asset_class = 'Equity')
WHERE mf.created_by_id = %s AND msip.active = True
group by mfsi.stock_name
order by 2 desc
'''

SIP_SECTOR_SHARES='''
select mfsi.sector as "Sector", sum(mfsi.holdings_percent * msip.amount * mfasset.percentage) as "Share"
from portfolio_mutualfund mf
    inner join portfolio_mutualfundsip msip on mf.id = msip.mutual_fund_id
    inner join mutualFund_mutualfundequityallocation mfsi on mf.mutual_fund_global_id = mfsi.mutual_fund_id
    inner join mutualFund_mutualfundassetallocation mfasset on (mfasset.mutual_fund_id = mf.mutual_fund_global_id and mfasset.asset_class = 'Equity')
WHERE mf.created_by_id = %s AND msip.active = True
group by mfsi.sector
order by 2 desc
'''

SIP_POPULAR_STOCKS='''
select mfsi.stock_name as "Stock Name", avg(mfsi.holdings_percent) * count(*) * 100 as popularity
from portfolio_mutualfund mf
       inner join mutualFund_mutualfundequityallocation mfsi on mf.mutual_fund_global_id = mfsi.mutual_fund_id
       inner join (select distinct mutual_fund_id from portfolio_mutualfundsip where active = true) mfsip
         on mfsip.mutual_fund_id = mf.id
WHERE mf.created_by_id = %s
group by mfsi.stock_name
having count(*) > 3
order by 2 desc
limit 20
'''

SIP_REBALANCE_ACTIVITIES='''
select re_balance_id, min(created_at), sum(amount) from portfolio_siprebalance
where created_by_id = %s
group by re_balance_id order by 2 desc
'''

SIP_REBALANCE_STOCK_SHARES='''
select mfsi.stock_name as "Stock Name", sum(mfsi.holdings_percent * msip.amount * mfasset.percentage) as "Share"
from portfolio_siprebalance msip
       inner join mutualFund_mutualfundequityallocation mfsi on msip.mutual_fund_global_id = mfsi.mutual_fund_id
       inner join mutualFund_mutualfundassetallocation mfasset
         on (mfasset.mutual_fund_id = msip.mutual_fund_global_id and mfasset.asset_class = 'Equity')
WHERE msip.re_balance_id = %s
group by mfsi.stock_name
order by 2 desc
'''

SIP_REBALANCE_SECTOR_SHARES='''
select mfsi.sector as "Sector", sum(mfsi.holdings_percent * msip.amount * mfasset.percentage) as "Share"
from portfolio_siprebalance msip
    inner join mutualFund_mutualfundequityallocation mfsi on msip.mutual_fund_global_id = mfsi.mutual_fund_id
    inner join mutualFund_mutualfundassetallocation mfasset on (mfasset.mutual_fund_id = msip.mutual_fund_global_id and mfasset.asset_class = 'Equity')
WHERE msip.re_balance_id = %s
group by mfsi.sector
order by 2 desc
'''