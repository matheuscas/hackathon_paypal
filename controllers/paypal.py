from applications.paypal_hackathon.modules import requests
import re

def index():
	return dict()

def compras_escolha_itens():
	response.title = 'Simulacao da escolha dos itens'
	return dict()	

def assinaturas_escolha_itens():
	response.title = 'Simulacao da escolha da assinatura'
	return dict()

def compras_finalizacao():
	response.title = 'PayPal na finalizacao da compra'
	return dict()

def pagina_produto():
	return dict()

def pagina_assinatura():
	return dict()		

def estorno():
	response.title = 'Estorno de transacao'
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

	return dict(details=details)

def assinaturas_retorno():
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

	return dict(details=details)	


def set_express_checkout():
	basic_data = basic_request
	return_url = url_prefix_sandbox + str(URL("paypal","compras_retorno"))
	cancel_url = url_prefix_sandbox + str(URL("paypal","compras_escolha_itens"))
	express_checkout_data = {
    	'METHOD':'SetExpressCheckout',
    	'PAYMENTREQUEST_0_PAYMENTACTION':'SALE',
    	'PAYMENTREQUEST_0_CURRENCYCODE':'BRL',
		'PAYMENTREQUEST_0_AMT':'721.00',
		'PAYMENTREQUEST_0_ITEMAMT':'721.00',
		'L_PAYMENTREQUEST_0_NAME0' : 'Item 1',
	    'L_PAYMENTREQUEST_0_DESC0' : 'Tablet Phaser Kinno II PC713 com Tela 7"',
	    'L_PAYMENTREQUEST_0_AMT0' : '236.00',
	    'L_PAYMENTREQUEST_0_QTY0' : '2',
	    'L_PAYMENTREQUEST_0_ITEMAMT' : '472.00',
	    'L_PAYMENTREQUEST_0_NAME1' : 'Item 2',
	    'L_PAYMENTREQUEST_0_DESC1' : 'Celular Desbloqueado CCE Motion Plus SK351 Preto com Dual Chip',
	    'L_PAYMENTREQUEST_0_AMT1' : '249.00',
	    'L_PAYMENTREQUEST_0_QTY1' : '1',
	    'RETURNURL' : return_url,
    	'CANCELURL' : cancel_url
	}

	basic_data.update(express_checkout_data)
	r = requests.get(sandbox, params=basic_data)
	res = r.text.split('&')
	token_part = res[0]
	token = token_part.split('=')[1]
	#return A('clique aqui', _href=paypalURL+'?'+'cmd=_express-checkout&token='+token)
	#teste = 'https://www.sandbox.paypal.com/incontext?token='+token
	redirect(paypalURL+'?'+'cmd=_express-checkout&token='+token)
	#redirect(teste)

def set_express_checkout_to_subscription():
	basic_data = basic_request
	return_url = url_prefix_sandbox + str(URL("paypal","assinaturas_retorno"))
	cancel_url = url_prefix_sandbox + str(URL("paypal","assinaturas_escolha_itens"))
	express_checkout_data = {
    	'METHOD':'SetExpressCheckout',
    	'PAYMENTREQUEST_0_PAYMENTACTION':'SALE',
    	'PAYMENTREQUEST_0_CURRENCYCODE':'BRL',
		'PAYMENTREQUEST_0_AMT':'100.00',
		'PAYMENTREQUEST_0_ITEMAMT':'100.00',
		'L_PAYMENTREQUEST_0_NAME0' : '1',
	    'L_PAYMENTREQUEST_0_DESC0' : 'Revista Info',
	    'L_PAYMENTREQUEST_0_AMT0' : '100.00',
	    'L_PAYMENTREQUEST_0_QTY0' : '1',

	    'L_PAYMENTREQUEST_0_ITEMCATEGORY0' : 'Digital', 
	    'L_BILLINGTYPE0' : 'RecurringPayments',
	    'L_BILLINGAGREEMENTDESCRIPTION0' : 'Revista Info',

	    'RETURNURL' : return_url,
    	'CANCELURL' : cancel_url
	}	

	basic_data.update(express_checkout_data)
	r = requests.get(sandbox, params=basic_data)
	res = r.text.split('&')
	token_part = res[0]
	token = token_part.split('=')[1]
	redirect(paypalURL+'?'+'cmd=_express-checkout&token='+token)

def do_express_checkout():
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
		'L_PAYMENTREQUEST_0_NAME1':request.vars['L_PAYMENTREQUEST_0_NAME1'],
		'L_PAYMENTREQUEST_0_DESC1':request.vars['L_PAYMENTREQUEST_0_DESC1'],
		'L_PAYMENTREQUEST_0_AMT1':request.vars['L_PAYMENTREQUEST_0_AMT1'],
		'L_PAYMENTREQUEST_0_QTY1':request.vars['L_PAYMENTREQUEST_0_QTY1'],
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

def set_express_checkout_product_page():
	basic_data = basic_request
	return_url = url_prefix_sandbox + str(URL("paypal","product_page_retorno"))
	cancel_url = url_prefix_sandbox + str(URL("paypal","pagina_produto"))
	express_checkout_data = {
    	'METHOD':'SetExpressCheckout',
    	'PAYMENTREQUEST_0_PAYMENTACTION':'SALE',
    	'PAYMENTREQUEST_0_CURRENCYCODE':'BRL',
		'PAYMENTREQUEST_0_AMT':'236.00',
		'PAYMENTREQUEST_0_ITEMAMT':'236.00',
		'L_PAYMENTREQUEST_0_NAME0' : 'Item 1',
	    'L_PAYMENTREQUEST_0_DESC0' : 'Tablet Phaser Kinno II PC713 com Tela 7"',
	    'L_PAYMENTREQUEST_0_AMT0' : '236.00',
	    'L_PAYMENTREQUEST_0_QTY0' : '1',
	    'RETURNURL' : return_url,
    	'CANCELURL' : cancel_url
	}

	basic_data.update(express_checkout_data)
	r = requests.get(sandbox, params=basic_data)
	res = r.text.split('&')
	token_part = res[0]
	token = token_part.split('=')[1]
	redirect(paypalURL+'?'+'cmd=_express-checkout&token='+token)	

def product_page_retorno():	
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

	return dict(details=details)



def do_express_checkout_product_page():
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

def create_recurring_payments_profile():
	basic_data = basic_request
	recurring_payments_data = {
    	'METHOD':'CreateRecurringPaymentsProfile',
		'TOKEN':request.vars['TOKEN'],
		'PAYERID':request.vars['PAYERID'],

		'PROFILESTARTDATE': request.now,
	    'DESC': 'Revista Info',
	    'BILLINGPERIOD': 'Day',
	    'BILLINGFREQUENCY': '1',
	    'AMT': 100,
	    'CURRENCYCODE': 'BRL',
	    'COUNTRYCODE': 'BR',
	    'MAXFAILEDPAYMENTS': 3
	}

	basic_data.update(recurring_payments_data)
	r = requests.get(sandbox, params=basic_data)
	return dict(details=__response_details_to_dict(r.text))

def refund():	
	basic_data = basic_request
	refund_data = {
		'METHOD':'RefundTransaction', 
    	'TRANSACTIONID' : request.vars.transaction,
    	'REFUNDTYPE' : 'Full'
	}
	basic_data.update(refund_data)
	r = requests.get(sandbox, params=basic_data)
	return dict(details=__response_details_to_dict(r.text))

def __response_details_to_dict(raw_text_response):
	splited = raw_text_response.split('&')
	dictt = {}
	for part in splited:
		key = part.split('=')[0]
		value = part.split('=')[1].replace('%2e','.')
		value = value.replace('%20',' ')
		value = value.replace('%40','@')
		value = value.replace('%2d','-')
		value = value.replace('%3a',':')
		dictt[key] = value

	return dictt

def ipn_post():
	if request.vars.test_ipn and request.vars.test_ipn == '1':
		endpoint = '/cgi-bin/webscr?cmd=_notify-validate'
		r = requests.get(paypalURL + endpoint, params=request.vars)
		if 'VERIFIED' in r.text:
			rows = db(db.ipn.chave == request.vars.hash).select()
			if len(rows) == 0:
				db.ipn.insert(txn_id=request.vars.txn_id,
							txn_type=request.vars.txn_type,
							receiver_email=request.vars.receiver_email,
							payment_status=request.vars.payment_status,
							pending_reason=request.vars.pending_reason,
							reason_code=request.vars.reason_code,
							custom=request.vars.payment_status,
							invoice=request.vars.invoice,
							notification=request.vars.notification
					)

def ipn_get():
	return dict(rows=db(db.ipn.id > 0).select())			
						