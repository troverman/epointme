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
    exhange_call_list = db(db.exchange_call).select()
    exhange_put_list = db(db.exchange_put).select()

    return dict(
        market_list=market_list,
        exhange_call_list=exhange_call_list,
        exhange_put_list=exhange_put_list,
    )

########################
####feed################
########################
def feed():
    return dict()

########################
####index###############
########################
def index():
    response.flash = T("cracking open the idea of fiat based value")
    item_post_list = db(db.item_post).select().as_list()
    market_list = db(db.market).select()

    #import random
    #random_five_items = random.shuffle(item_post_list)[:5]
    return dict(
        item_post_list=item_post_list,
        market_list=market_list
    )

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
        exhange_call_list = db(db.exchange_call.market_buy == market_from_url['id']).select()
        exhange_put_list = db(db.exchange_put.market_sell == market_from_url['id']).select()




        item_post_list = db(db.item_post).select()
        item_post_market_list=[]
        item_post_market_list1=[]

        for item in item_post_list:
            for market_id in item['market_array']:
                market_array = market_id.split(',')
                item_post_market_list1.append(market_array[0])
                if market_array[0] == market_from_url['id']:
                    item_post_market_list1.append(item)    



    except IndexError:
        redirect(URL('markets'))
    return dict(
        market_from_url=market_from_url,
        transaction_array=transaction_array,
        market_circulation_size=market_circulation_size,
        exhange_call_list=exhange_call_list,
        exhange_put_list=exhange_put_list,
        item_post_market_list1=item_post_market_list1,
    )

########################
####markets#############
########################
def markets():

    market_list = db(db.market).select()

    form_create_market = SQLFORM(db.market)
    if form_create_market.process(formname='form_create_market').accepted:
        session.flash = 'market created'
        redirect(URL('/market/'))        
    elif form_create_market.errors:
        response.flash = 'Error'
    return dict(
        market_list=market_list,
        form_create_market=form_create_market,
    )

########################
####marketplace#########
########################
def marketplace():
    item_post_list = db(db.item_post).select()
    item_post_tag_list = []
    item_post_market_list = []

    item_post_market_list1 = []

    for count, item in enumerate(item_post_list):
        item_post_tag_list.append(db(db.item_post_tag.item_post_id == item['id']).select())
        item_post_market_list.append([])
        for market_id in item['market_array']:
            market_array = market_id.split(',')
            item_post_market_list[count].append([db(db.market.id == market_array[0]).select(), market_array[1]])
        item_post_market_list1.append([item,item_post_market_list[count]])

    item_post_tag_list_array = []
    for tag_list in item_post_tag_list:
        for tag in tag_list:
            item_post_tag_list_array.append(tag['tag'])   





    set_item_post_tag_list = set(item_post_tag_list_array)
    tag_item_post_list_unsorted = list(set_item_post_tag_list)
    combined_count_and_tag_array=[]
    for tag in tag_item_post_list_unsorted:
        combined_count_and_tag_array.append([tag, item_post_tag_list_array.count(tag)])
    from operator import itemgetter
    tag_item_post_list_sorted_by_total_count = sorted(combined_count_and_tag_array, key=itemgetter(1))  


    
    form_create_marketplace_item = SQLFORM(db.item_post)
    if form_create_marketplace_item.process(formname='form_create_marketplace_item').accepted:
        session.flash = 'item posted'
        redirect(URL('/marketplace/'))        
    elif form_create_marketplace_item.errors:
        response.flash = 'Error'

    return dict(
        item_post_market_list=item_post_market_list,
        item_post_list=item_post_list,
        form_create_marketplace_item=form_create_marketplace_item,
        tag_item_post_list_sorted_by_total_count=tag_item_post_list_sorted_by_total_count,
        item_post_market_list1=item_post_market_list1,
    )

########################
####member##############
########################
def member():
    try:
        member_from_url = db(db.auth_user.username == request.args(0)).select()[0]
        sent_transaction_from_member = db(db.transaction.member_send == member_from_url['id']).select()
        recieve_transaction_from_member = db(db.transaction.member_recieve == member_from_url['id']).select()

        recieve_market_array = []
        for transaction in recieve_transaction_from_member:
            recieve_market_array.append(transaction['market_id'])

        recieve_market_set_array = set(recieve_market_array)


    except IndexError:
        redirect(URL('members'))
    return dict(
        member_from_url=member_from_url,
        sent_transaction_from_member=sent_transaction_from_member,
        recieve_transaction_from_member=recieve_transaction_from_member,
        recieve_market_set_array=recieve_market_set_array,
    )

########################
####mission#############
########################
def mission():
    return dict()

########################
####notifications#######
########################
def notifications():
    return dict()

########################
####pointbank###########
########################
def pointbank():
    return dict()

########################
####search##############
########################
def search():
    return dict()

########################
####thread##############
########################
def thread():
    thread_by_url = db(db.item_post.url_title == request.args(0)).select()    
    thread_tag = db(db.item_post_tag.item_post_id == thread_by_url[0]['id']).select()
    similar_threads = db(db.item_post).select()    

    form_create_comment_root = SQLFORM(db.item_post_comment)
    if form_create_comment_root.process(formname='form_create_comment_root').accepted:    
        db(db.item_post_comment.id==form_create_comment_root.vars.id).update(user_id=auth.user_id)
        db(db.item_post_comment.id==form_create_comment_root.vars.id).update(item_post_id=thread_by_url[0]['id'])
        session.flash = 'Commented'
        redirect(URL('/thread/' + request.args(0)))       
    elif form_create_comment_root.errors:
        session.flash = 'Error'   
        redirect(URL(''))
     
    create_comment_with_id_dict = dict()  
    item_post_comments = db(db.item_post_comment.item_post_id == thread_by_url[0]['id']).select()
    for comment in item_post_comments:  
        create_comment_with_id_dict[comment['id']] = SQLFORM(db.item_post_comment)
        if create_comment_with_id_dict[comment['id']].process(formname='create_comment_with_id_dict' + str(comment['id'])).accepted: 
            db(db.item_post_comment.id==create_comment_with_id_dict[comment['id']].vars.id).update(user_id=auth.user_id)
            db(db.item_post_comment.id==create_comment_with_id_dict[comment['id']].vars.id).update(item_post_id=thread_by_url[0]['id'])
            session.flash = 'Commented'
            redirect(URL('/thread/' + request.args(0)))
        elif create_comment_with_id_dict[comment['id']].errors:
            session.flash = 'Error'   
            redirect(URL(''))



    return dict(
        create_comment_with_id_dict=create_comment_with_id_dict,
        form_create_comment_root=form_create_comment_root,
        thread_by_url=thread_by_url,
        thread_tag=thread_tag,
        similar_threads=similar_threads,
    )

########################
####transaction#########
########################
def transaction():
    return dict()

########################
####transactions########
########################
def transactions():
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
        db.transaction.insert(member_recieve='5261841206870016',member_send=member['id'], market_id='6559908098998272', amount='1')

    return dict()    

@cache.action()
def download():
    return response.download(request, db)


def call():
    return service()


@auth.requires_signature()
def data():
    return dict(form=crud())


################################################################
####ajax########################################################
################################################################

################################
####ajax_sort_post_by_date######
################################ 
def ajax_sort_post_by_date(): 

    #from operator import itemgetter
    #tag_collection_list_sorted_by_total_count = sorted(combined_count_and_tag_array, key=itemgetter(1))               
  
    jquery = "jQuery('.flash').html('%s').slideDown().delay(1000).slideUp();" % 'hi'

    return jquery
