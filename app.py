# -*- coding: utf-8 -*-
import os
import httplib
import base64
import json
import urllib
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# when testing if you want to point to a separate ctm domain
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.config.update(dict(
  DEBUG=True,
  SECRET_KEY='Update to something secure',
  CTM_AUTH=base64.standard_b64encode('%s:%s' % (os.environ['CTM_TOKEN'], os.environ['CTM_TOKEN'])), # get these from your CTM agency settings page
  CTM_HOST=os.environ['CTM_HOST'] # api.calltrackingmetrics.com
))

def ctm_get(endpoint, query=dict()):
  conn = httplib.HTTPSConnection(app.config['CTM_HOST'])
  headers = { 'Authorization' : 'Basic %s' %  app.config['CTM_AUTH'] }
  conn.request("GET","/api/v1/" + endpoint + ".json?" + urllib.urlencode(query,True), headers=headers)
  res = conn.getresponse()
  print res.status, res.reason
  if res.status == 200:
    return json.load(res)

def ctm_post(endpoint, post_body=dict()):
  conn = httplib.HTTPSConnection(app.config['CTM_HOST'])
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
  if not g.account_id and request.endpoint != 'show_accounts' and request.endpoint != 'change_accounts':
    flash('Choose an account to get started')
    return redirect(url_for('show_accounts'))

@app.route('/accounts')
def show_accounts():
  pager = ctm_get('accounts', {'limit_fields[]': ['name', 'id']})
  accounts = pager['accounts']
  return render_template('show_accounts.html', accounts=accounts)

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
  return redirect(url_for('show_calls'))

@app.route('/accounts/<int:account_id>')
def change_accounts(account_id):
  session['account_id'] = account_id
  account = ctm_get('accounts/%d' % account_id)
  session['account_name'] = account['name']
  return redirect(url_for('show_calls'))

@app.route('/')
def show_calls():
  page = request.args.get('page')

  pager = ctm_get('/accounts/%d/calls' % g.account_id, {'page': page}) 

  return render_template('show_calls.html', pager=pager)

@app.route('/numbers')
def show_numbers():
  page = request.args.get('page')

  pager = ctm_get('/accounts/%d/numbers' % g.account_id, {'page': page}) 
  print json.dumps(pager)

  return render_template('show_numbers.html', pager=pager)

@app.route('/numbers/<number_id>/edit')
def edit_number(number_id):

  number = ctm_get('/accounts/%d/numbers/%s' % (g.account_id, number_id)) 

  if number['route_to'] == 'menu':
    print "menu"
  elif number['route_to'] == 'geo':
    print "geo"

  return render_template('edit_number.html', number=number)

@app.route('/numbers/<number_id>', methods=['POST'])
def update_number(number_id):
  data = dict({'name': request.form['name']})
  dial_route = request.form['route_to']

  print request.form

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
    data['number_ids'] = request.form['route_object']

  data['tracking_source_id'] = request.form['source']
  data['dial_route'] = dial_route

  number = ctm_post('accounts/%d/numbers/%s/update_number' % (g.account_id, number_id), data)
  flash('Updated Phone Number Routing')
  return redirect(url_for('edit_number', number_id=number_id))

@app.route('/lookup/<object_type>')
def lookup_object(object_type):
  search = request.args.get('q')
  objects = ctm_get('/accounts/%d/lookup' % g.account_id, {'object_type': object_type, 'search': search})
  return json.dumps(objects)

if __name__ == "__main__":
  app.run()
