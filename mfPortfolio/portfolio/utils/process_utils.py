from .common_enums import SIPFrequency

SIP_EVENT_PREFIX = 'PORTFOLIO_SIP_EVENT_'

MONTHLY_SIP_CREATE_EVENT_TEMPLATE = '''
CREATE EVENT %s
    ON SCHEDULE
      EVERY 1 MONTH
      STARTS TIMESTAMP('%s')
    DO
        UPDATE portfolio_mutualfund mf
            inner join portfolio_mutualfundsip sip
          on(mf.id = sip.mutual_fund_id AND sip.id = %s)
        SET mf.last_transaction_date = curdate(), mf.amount = mf.amount + sip.amount, sip.last_transaction_date = curdate();'''

QUARTERLY_SIP_CREATE_EVENT_TEMPLATE = '''
CREATE EVENT %s
    ON SCHEDULE
      EVERY 15 DAY
      STARTS TIMESTAMP('%s')
    DO
        UPDATE portfolio_mutualfund mf
            inner join portfolio_mutualfundsip sip
          on(mf.id = sip.mutual_fund_id AND sip.id = %s)
        SET mf.last_transaction_date = curdate(), mf.amount = mf.amount + sip.amount, sip.last_transaction_date = curdate();'''

WEEKLY_SIP_CREATE_EVENT_TEMPLATE = '''
CREATE EVENT %s
    ON SCHEDULE
      EVERY 1 WEEK
      STARTS TIMESTAMP('%s')
    DO
        UPDATE portfolio_mutualfund mf
            inner join portfolio_mutualfundsip sip
          on(mf.id = sip.mutual_fund_id AND sip.id = %s)
        SET mf.last_transaction_date = curdate(), mf.amount = mf.amount + sip.amount, sip.last_transaction_date = curdate();'''


SIP_DROP_EVENT_TEMPLATE = 'drop event if exists %s;'


def build_sip_create_event(sip_id, start_date, frequency):
    start_date_str = start_date.strftime('%Y-%m-%d')
    event_name = SIP_EVENT_PREFIX + str(sip_id)
    sip_create_sql = None

    if SIPFrequency.MONTHLY.value == frequency:
        sip_create_sql = MONTHLY_SIP_CREATE_EVENT_TEMPLATE % (event_name, start_date_str, sip_id)
    elif SIPFrequency.QUARTERLY.value == frequency:
        sip_create_sql = QUARTERLY_SIP_CREATE_EVENT_TEMPLATE % (event_name, start_date_str, sip_id)
    elif SIPFrequency.WEEKLY.value == frequency:
        sip_create_sql = WEEKLY_SIP_CREATE_EVENT_TEMPLATE % (event_name, start_date_str, sip_id)
    else:
        raise ValueError('Unknown frequency: ' + frequency)
    return sip_create_sql


def build_sip_delete_event(sip_id):
    event_name = SIP_EVENT_PREFIX + str(sip_id)
    return SIP_DROP_EVENT_TEMPLATE % event_name


