################################################################
####menu.py#####################################################
################################################################

################################
####title#######################
################################  
if request.function == 'index':
    response.title = 'epoint.me'
else:
    response.title = request.function
response.logo = A(B('epoint.me'), _class="brand",_href="http://www.epoint.me/")

################################
####meta########################
################################ 
response.meta.author = 'Trevor Overman'
response.meta.description = 'epoint.me'
response.meta.keywords = 'epoint, value, market, giving, transparent'
response.meta.generator = 'epoint.me'
