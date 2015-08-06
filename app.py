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
  print res
  if not res:
    flash('Failed to create your account')
    return render_template('new_account.html')

  session['account_id'] = res['id']
  return redirect(url_for('show_calls'))

@app.route('/accounts/<int:account_id>')
def change_accounts(account_id):
  session['account_id'] = account_id
  return redirect(url_for('show_calls'))

@app.route('/')
def show_calls():
  account_id = session.get('account_id')
  if not account_id:
    flash('Choose an account to get started')
    return redirect(url_for('show_accounts'))

  page = request.args.get('page')

  pager = ctm_get('/accounts/%d/calls' % account_id, {'page': page}) 

  return render_template('show_calls.html', pager=pager)

if __name__ == "__main__":
  app.run()
