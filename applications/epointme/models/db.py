################################################################
####db.py#######################################################
################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

################################
####database_conntection########
################################  

## connect to Google BigTable (optional 'google:datastore://namespace')
db = DAL('google:datastore')
## store sessions and tickets there
session.connect(request, response, db=db)
## or store session in Memcache, Redis, etc.
## from gluon.contrib.memdb import MEMDB
## from google.appengine.api.memcache import Client
## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'


from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

auth.define_tables(username=True, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'mail@deliveryfor.com'
mail.settings.login = ''

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
db.auth_user.first_name.readable = False
db.auth_user.last_name.readable = False 

################################################################
####database_tables#############################################
################################################################

################################
####exchange_sell###############
################################ 
db.define_table('exchange_put',
   Field('creator_id', 'string', readable=False, writable=False),
   Field('market_sell', 'string'),
   Field('amount_sell', 'string'),
   Field('market_buy', 'string'),
   Field('amount_buy', 'string'),
   Field('call_expiration', 'datetime'),

)

################################
####exchange_buy################
################################ 
db.define_table('exchange_call',
   Field('creator_id', 'string', readable=False, writable=False),
   Field('market_buy', 'string'),
   Field('amount_buy', 'string'),
   Field('market_sell', 'string'),
   Field('amount_sell', 'string'),
   Field('put_expiration', 'datetime'),

)

################################
####item_post###################
################################ 
db.define_table('item_post',
   Field('creator_id', 'string', readable=False, writable=False),
   Field('item_detail', 'string'),
   Field('item_post_time', 'datetime', default=request.now),
   Field('url_title', 'string'),
   Field('title', 'string'),
   Field('item_content', 'string'),
   Field('market_array', 'list:string'),
)

################################
####item_post_comment###########
################################ 
db.define_table('item_post_comment',
    Field('user_id','reference auth_user', default=auth.user_id, readable=False, writable=False),
    Field('item_post_id','string', readable=False, writable=False),
    Field('parent_comment_id','string', readable=False, writable=False),
    Field('comment_content','string'),
)

################################
####item_post_image#############
################################
db.define_table('item_post_image',
    Field('item_post_id', 'string', readable=False, writable=False),
    Field('picture', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob')
)

################################
####item_post_tag###############
################################ 
db.define_table('item_post_tag',
   Field('item_post_id', 'string', readable=False, writable=False),
   Field('creator_id', 'string' , readable=False, writable=False),
   Field('tag', 'string'),
)

################################
####market######################
################################ 
db.define_table('market',
   Field('creator_id', 'string', readable=False, writable=False),
   Field('url_title', 'string'),
   Field('title', 'string'),
   Field('description', 'string'),
)

################################
####transaction#################
################################ 
db.define_table('transaction',
   Field('time_stamp','datetime',default=request.now,writable=False,readable=False), 
   Field('member_send', 'string', readable=False, writable=False),
   Field('member_recieve', 'string', readable=False, writable=False),
   Field('market_id', 'string'),
   Field('amount', 'string'),
)


