########################
####about###############
########################
def about():
    return dict()

########################
####account#############
########################
def account():
    return dict()

########################
####exchange############
########################
def exchange():
    market_list = db(db.market).select()
    exhange_list = db(db.exchange_put).select()

    return dict(
        market_list=market_list,
        exhange_list=exhange_list,
    )

########################
####index###############
########################
def index():
    response.flash = T("cracking open the idea of fiat based value")
    return dict()

########################
####market##############
########################
def market():
    import time
    try:
        market_from_url = db(db.market.url_title == request.args(0)).select()[0]
        transaction_from_market = db(db.transaction.market_id == market_from_url['id']).select()
        transaction_array=[]
        transaction_from_market_pb = db((db.transaction.market_id == market_from_url['id']) & (db.transaction.member_send == '5261841206870016')).select()
        market_circulation_size = 0
        for transaction in transaction_from_market_pb:
            market_circulation_size += int(transaction['amount'])
        for transaction in transaction_from_market:
            transaction_array.append([db(db.auth_user.id == transaction['member_send']).select()[0], db(db.auth_user.id == transaction['member_recieve']).select()[0], time.mktime(transaction['time_stamp'].timetuple())*1000
, transaction['amount']])
                


    except IndexError:
        redirect(URL('markets'))
    return dict(
        market_from_url=market_from_url,
        transaction_array=transaction_array,
        market_circulation_size=market_circulation_size,
    )

########################
####markets#############
########################
def markets():

    market_list = db(db.market).select()
    return dict(market_list=market_list)

########################
####marketplace#########
########################
def marketplace():
    item_post_list = db(db.item_post).select()
    return dict(
        item_post_list=item_post_list,
    )

########################
####member##############
########################
def member():
    try:
        member_from_url = db(db.auth_user.username == request.args(0)).select()[0]
        sent_transaction_from_member = db(db.transaction.member_send == member_from_url['id']).select()
        recieve_transaction_from_member = db(db.transaction.member_recieve == member_from_url['id']).select()

    except IndexError:
        redirect(URL('members'))
    return dict(
        member_from_url=member_from_url,
        sent_transaction_from_member=sent_transaction_from_member,
        recieve_transaction_from_member=recieve_transaction_from_member,
    )

########################
####pointbank###########
########################
def pointbank():
    return dict()

########################
####transparency########
########################
def transparency():
    transaction_array = db(db.transaction).select()
    return dict(transaction_array=transaction_array)

########################
####update_market_daily#
########################
def update_market_daily():

    member_list = db(db.auth_user).select()
    for member in member_list:
        db.transaction.insert(member_recieve=member['id'],member_send='5261841206870016', market_id='5768062158503936', amount='1')
        db.transaction.insert(member_recieve=member['id'],member_send='5261841206870016', market_id='4985726349344768', amount='1000')

    return dict()    

@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()


@auth.requires_signature()
def data():
    return dict(form=crud())
