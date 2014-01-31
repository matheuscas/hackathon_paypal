from applications.paypal_hackathon.modules import requests
import re

def index():
	return dict()

def compras_escolha_itens():
	print request.url
	response.title = 'Simulacao da escolha dos itens'
	return dict()	

def compras_finalizacao():
	response.title = 'PayPal na finalizacao da compra'
	return dict()	

def compras_retorno():	
	get_express_checkout_data = {
		'SUBJECT': paypal_email_id,
		'METHOD':'GetExpressCheckoutDetails',
		'TOKEN':request.vars.token
	}

	complete_data = basic_request
	complete_data.update(get_express_checkout_data)
	r = requests.get(sandbox, params=complete_data)
	details = __response_details_to_dict(r.text)
	details['TOKEN'] = request.vars.token

	print'-------------compras_retorno'
	print details['PAYMENTREQUEST_0_AMT']
	#print details['L_PAYMENTREQUEST_0_AMT0']
	#print details['L_PAYMENTREQUEST_0_ITEMAMT']


	return dict(details=details)


def set_express_checkout():
	basic_data = basic_request
	url_prefix = 'http://127.0.0.1:8000'
	return_url = url_prefix + str(URL("paypal","compras_retorno"))
	cancel_url = url_prefix + str(URL("paypal","compras_escolha_itens"))
	express_checkout_data = {
    	'METHOD':'SetExpressCheckout',
    	'PAYMENTREQUEST_0_PAYMENTACTION':'SALE',
    	'PAYMENTREQUEST_0_CURRENCYCODE':'BRL',
		'PAYMENTREQUEST_0_AMT':'56.76',
		'PAYMENTREQUEST_0_ITEMAMT':'56.76',
		'L_PAYMENTREQUEST_0_NAME0' : 'Item A',
	    'L_PAYMENTREQUEST_0_DESC0' : 'Produto A – 110V',
	    'L_PAYMENTREQUEST_0_AMT0' : '56.76',
	    'L_PAYMENTREQUEST_0_QTY0' : '1',
	    'L_PAYMENTREQUEST_0_ITEMAMT' : '56.76',
	    'RETURNURL' : return_url,
    	'CANCELURL' : cancel_url
	}

	print '-----------------------------------do'
	print express_checkout_data['PAYMENTREQUEST_0_AMT']
	print express_checkout_data['L_PAYMENTREQUEST_0_AMT0']
	print express_checkout_data['L_PAYMENTREQUEST_0_ITEMAMT']

	basic_data.update(express_checkout_data)
	r = requests.get(sandbox, params=basic_data)
	res = r.text.split('&')
	token_part = res[0]
	token = token_part.split('=')[1]
	redirect(paypalURL+'?'+'cmd=_express-checkout&token='+token)

def do_express_checkout():
	print '-----------------------------------do_express_checkout'
	print request.vars['PAYMENTREQUEST_0_AMT']
	print request.vars['L_PAYMENTREQUEST_0_AMT0']
	print request.vars['L_PAYMENTREQUEST_0_ITEMAMT']
	basic_data = basic_request
	do_express_data = {
		'METHOD':'DoExpressCheckoutPayment',
		'TOKEN':request.vars['TOKEN'],
		'PAYERID':request.vars['PAYERID'],
		'PAYMENTREQUEST_0_PAYMENTACTION' : 'SALE',
		'PAYMENTREQUEST_0_AMT':request.vars['PAYMENTREQUEST_0_AMT'],
		'PAYMENTREQUEST_0_CURRENCYCODE':request.vars['PAYMENTREQUEST_0_CURRENCYCODE'],
		'PAYMENTREQUEST_0_ITEMAMT':request.vars['PAYMENTREQUEST_0_ITEMAMT'],
		'L_PAYMENTREQUEST_0_NAME0':request.vars['L_PAYMENTREQUEST_0_NAME0'],
		'L_PAYMENTREQUEST_0_DESC0':request.vars['L_PAYMENTREQUEST_0_DESC0'],
		'L_PAYMENTREQUEST_0_AMT0':request.vars['L_PAYMENTREQUEST_0_AMT0'],
		'L_PAYMENTREQUEST_0_QTY0':request.vars['L_PAYMENTREQUEST_0_QTY0'],
		'L_PAYMENTREQUEST_0_ITEMAMT':request.vars['L_PAYMENTREQUEST_0_ITEMAMT'],
		'PAYMENTREQUEST_0_SHIPTONAME' : request.vars['PAYMENTREQUEST_0_SHIPTONAME'],
		'PAYMENTREQUEST_0_SHIPTOSTREET' : request.vars['PAYMENTREQUEST_0_SHIPTOSTREET'],
		'PAYMENTREQUEST_0_SHIPTOSTREET2' : request.vars['PAYMENTREQUEST_0_SHIPTOSTREET2'],
		'PAYMENTREQUEST_0_SHIPTOCITY' : request.vars['PAYMENTREQUEST_0_SHIPTOCITY'],
		'PAYMENTREQUEST_0_SHIPTOSTATE' : request.vars['PAYMENTREQUEST_0_SHIPTOSTATE'],
		'PAYMENTREQUEST_0_SHIPTOZIP' : request.vars['PAYMENTREQUEST_0_SHIPTOZIP'],
		'PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE' : request.vars['PAYMENTREQUEST_0_SHIPTOCOUNTRYCODE']
	}
	basic_data.update(do_express_data)
	r = requests.get(sandbox, params=basic_data)
	return dict(details=__response_details_to_dict(r.text))

def ipn():
	return dict()

def refund():
	return dict()

def __response_details_to_dict(raw_text_response):
	splited = raw_text_response.split('&')
	dictt = {}
	for part in splited:
		key = part.split('=')[0]
		value = part.split('=')[1].replace('%2e','.')
		dictt[key] = value

	return dictt						