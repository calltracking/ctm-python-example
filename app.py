# -*- coding: utf-8 -*-
# when testing if you want to point to a separate ctm domain
import ssl
import socket
import os
import httplib
import base64
import json
import urllib
import uuid
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)
app.config.update(dict(
  DEBUG=(os.environ['CTM_ENV'] == 'development'),
  SECRET_KEY='Update to something secure',
  CTM_AUTH=base64.standard_b64encode('%s:%s' % (os.environ['CTM_TOKEN'], os.environ['CTM_SECRET'])), # get these from your CTM agency settings page
  CTM_HOST=os.environ['CTM_HOST'] # api.calltrackingmetrics.com
))
socketio = SocketIO(app)

def get_http_conn():
  if app.config['DEBUG']:
    return httplib.HTTPSConnection(app.config['CTM_HOST'], 443, None, None, None, socket._GLOBAL_DEFAULT_TIMEOUT, None, ssl._create_unverified_context())
  return httplib.HTTPSConnection(app.config['CTM_HOST'])

def ctm_get(endpoint, query=dict()):
  conn = get_http_conn()
  headers = { 'Authorization' : 'Basic %s' %  app.config['CTM_AUTH'] }
  conn.request("GET","/api/v1/" + endpoint + ".json?" + urllib.urlencode(query,True), headers=headers)
  res = conn.getresponse()
  print res.status, res.reason
  if res.status == 200:
    return json.load(res)
  print res.read()

def ctm_post(endpoint, post_body=dict()):
  conn = get_http_conn()
  headers = { 'Authorization' : 'Basic %s' %  app.config['CTM_AUTH'] }
  conn.request("POST","/api/v1/" + endpoint + ".json", body=urllib.urlencode(post_body,True), headers=headers)
  res = conn.getresponse()
  print res.status, res.reason
  if res.status == 200:
    return json.load(res)
  print res.read()

@app.before_request
def verify_session():
  g.account_id   = session.get('account_id')
  g.account_name = session.get('account_name')

  if not g.account_id and request.endpoint != 'show_accounts' and request.endpoint != 'change_accounts' and request.endpoint != 'purchase_notify_event':
    flash('Choose an account to get started')
    return redirect(url_for('show_accounts'))

@app.route('/accounts')
def show_accounts():
  page = request.args.get('page')
  if not page:
    page = 1

  pager = ctm_get('accounts', {'limit_fields[]': ['name', 'id'], 'page': page})
  return render_template('show_accounts.html', pager=pager)

@app.route('/accounts/new')
def new_account():
  return render_template('new_account.html')

@app.route('/accounts/create', methods=['POST'])
def create_account():
  res = ctm_post("accounts", {'account[name]': request.form['name'],
                              'account[timezone]': request.form['timezone'],
                              'billing_type': 'existing'})
  if not res:
    flash('Failed to create your account')
    return render_template('new_account.html')

  session['account_id'] = res['id']
  return redirect(url_for('setup_google'))

@app.route('/accounts/<int:account_id>')
def change_accounts(account_id):
  session['account_id'] = account_id
  account = ctm_get('accounts/%d' % account_id)
  session['account_name'] = account['name']
  return redirect(url_for('show_calls'))

@app.route('/google/links')
def get_google_links():
  data = ctm_get('ga/links')
  return jsonify(data)

@app.route('/google/<int:account_id>/properties')
def get_google_property(account_id):
  data = ctm_get('accounts/%d/ga/link' % account_id)
  return jsonify(data)

@app.route('/google/setup')
def setup_google():
  return render_template('setup_google.html')

@app.route('/google/link', methods=['POST'])
def link_google():
  uacode = request.form['uacode']
  link_id = request.form['link_id']
  data = dict({'link_id': request.form['link_id'], 'default': uacode})
  ctm_post('accounts/%d/ga/link' % g.account_id, data)
  flash('Google Web Property now assigned to your account.')
  return redirect('/google/setup')

@app.route('/')
def show_calls():
  page = request.args.get('page')
  if not page:
    page = 1

  pager = ctm_get('/accounts/%d/calls' % g.account_id, {'page': page}) 

  return render_template('show_calls.html', pager=pager)

@app.route('/numbers')
def show_numbers():
  page = request.args.get('page')
  if not page:
    page = 1

  pager = ctm_get('/accounts/%d/numbers' % g.account_id, {'page': page}) 

  return render_template('show_numbers.html', pager=pager)

@app.route('/numbers/<number_id>/edit')
def edit_number(number_id):
  number = ctm_get('/accounts/%d/numbers/%s' % (g.account_id, number_id)) 

  return render_template('edit_number.html', number=number)

@app.route('/numbers/<number_id>', methods=['POST'])
def update_number(number_id):
  data = dict({'name': request.form['name']})
  dial_route = request.form['route_to']

  if   dial_route == 'voice_menu':
    data['voice_menu_id'] = request.form['route_object']
  elif dial_route == 'geo_config':
    data['geo_config_id'] = request.form['route_object']
  elif dial_route == 'call_queue':
    data['call_queue_id'] = request.form['route_object']
  elif dial_route == 'user':
    dial_route = 'call_agent'
    data['user_id'] = request.form['route_object']
  elif dial_route == 'receiving_number':
    dial_route = 'number'
    data['numbers_id[]'] = request.form.getlist('route_object[]')

  data['tracking_source_id'] = request.form['source']
  data['number_config_id'] = request.form['number_config_id']
  data['dial_route'] = dial_route

  number = ctm_post('accounts/%d/numbers/%s/update_number' % (g.account_id, number_id), data)
  flash('Updated Phone Number Routing')
  return redirect(url_for('edit_number', number_id=number_id))

@app.route('/numbers/new')
def new_number():
  return render_template('new_number.html') 

@app.route('/numbers/buy', methods=['POST'])
def buy_numbers():
  uid  = str(uuid.uuid1())
  data = dict({'status_url': request.url_root + 'numbers/purchase/' + uid,
               'number[]': request.form.getlist('numbers[]')})

  res  = ctm_post('accounts/%d/numbers/purchase' % g.account_id, data)

  return jsonify(data)

@app.route('/numbers/check/<id>')
def check_purchase():
  return jsonify({"status": "pending"})

# a status_url included when purchasing numbers that CTM will
# send allowing the server to notify the client about the order status
@app.route('/numbers/purchase/<id>', methods=['POST'])
def purchase_notify_event(id):
  print "socketio.emit#purchase"
  purchase = request.get_json(force=True)
  print purchase
  socketio.emit("purchase", purchase, namespace='/ctm')
  return jsonify({"status": "ack"})

@socketio.on('connect', namespace='/ctm')
def ctm_connect():
  emit('linked', {'data': 'Connected'})

@app.route('/numbers/search/<country>/<searchby>')
def search_numbers(country, searchby):
  # example query
  # https://api.calltrackingmetrics.com/api/v1/accounts/18614/numbers/search.json?country=DE&searchby=area&areacode=&pattern= 
  areacode = request.args.get('areacode')

  if not searchby or searchby == 'local':
    searchby = 'area'

  if not areacode:
    areacode = ''

  numbers = ctm_get('accounts/%d/numbers/search' % g.account_id, {'searchby': searchby, 'country': country, 'areacode': areacode})

  return jsonify(numbers)

@app.route('/settings')
def show_settings():
  page = request.args.get('page')
  if not page:
    page = 1

  pager = ctm_get('accounts/%d/call_settings' % g.account_id, {'page': page}) 

  return render_template('show_settings.html', pager=pager)

@app.route('/settings/<id>/edit')
def edit_settings(id):
  config = ctm_get('/accounts/%d/call_settings/%s' % (g.account_id, id))

  return render_template('edit_setting.html', config=config)

@app.route('/settings/<id>', methods=['POST'])
def update_setting(id):

  data = dict({'name': request.form['name'], 'play_message': request.form['play_message'], '_method': 'put'})

  if request.form['inbound_recordings_on']:
    data['inbound_recordings_on'] = 1

  if request.form['outbound_recording_on']:
    data['outbound_recording_on'] = 1

  if request.form['transcription']:
    data['transcription'] = 1

  if request.form['premium_callerid_enabled']:
    data['premium_callerid_enabled'] = 1

  setting = ctm_post('accounts/%d/call_settings/%s' % (g.account_id, id), data)

  flash('Updated Call Settings')

  return redirect(url_for('edit_settings', id=id))

@app.route('/menus', methods=['GET'])
def get_menus():
  page = request.args.get('page')
  if not page:
    page = 1
  pager = ctm_get('/accounts/%d/voice_menus' % g.account_id, {'page': page}) 
  return render_template('show_menus.html', pager=pager)

@app.route('/menus/<menu_id>/edit', methods=['GET'])
def edit_menu(menu_id):
  menu = ctm_get('/accounts/%d/voice_menus/%s' % (g.account_id, menu_id)) 
  return render_template('edit_menu.html', menu=menu)

@app.route('/menus/<menu_id>/items', methods=['GET'])
def show_menu_items(menu_id):
  data = ctm_get('/accounts/%d/voice_menus/%s/voice_menu_items' % (g.account_id, menu_id)) 
  return jsonify(data)

@app.route('/menus/<menu_id>', methods=['POST'])
def update_menu(menu_id):
  res = ctm_post("accounts/%d/voice_menus/%s" % (g.account_id, menu_id),
        {'voice_menu[name]':           request.form['name'],
         'voice_menu[timezone]':       request.form['play_message'],
         'voice_menu[prompt_retries]': request.form['prompt_retries'],
         'voice_menu[input_maxkeys]':  request.form['input_maxkeys'],
         'voice_menu[input_timeout]':  request.form['input_timeout']
        })
  if not res:
    flash('Failed to create your account')
    return render_template('new_account.html')

  session['account_id'] = res['id']
  return redirect(url_for('setup_google'))


# lookup a specific object e.g. voice menu, call queue, receiving number, etc...
@app.route('/lookup/<object_type>')
def lookup_object(object_type):
  search = request.args.get('q')
  if not search:
    search = ''

  objects = ctm_get('/accounts/%d/lookup' % g.account_id, {'object_type': object_type, 'search': search, 'idstr': '1'})
  return json.dumps(objects)

# lookup by id
@app.route('/lookup/<object_type>/<object_id>', methods=['GET'])
def lookup_object_ids(object_type, object_id):
  objects = ctm_get('/accounts/%d/lookupid' % g.account_id, {'object_type': object_type, 'object_id': object_id})
  return json.dumps(objects)

if __name__ == '__main__':
  socketio.run(app)
