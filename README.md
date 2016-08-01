CTM Python
----------

## Installation
```json
git clone https://github.com/calltracking/ctm-python-example.git
cd ctm-python-example
pip install flask
pip install flask-socketio
```

A CallTrackingMetrics agency account - signup here: https://www.calltrackingmetrics.com/plans

## Running the example application

You should configure your environment using agency or enterprise API keys

```bash
export CTM_ENV=development
export CTM_TOKEN=key
export CTM_SECRET=sec
export CTM_HOST=api.calltrackingmetrics.com

python app.py
```

You should now see something like this in the console
```bash
* Restarting with stat
* Debugger is active!
* Debugger pin code: 158-662-312
(95762) wsgi starting up on http://127.0.0.1:5000
```

If you open a browser and visit http://localhost:5000 you should see a menu with Accounts, Numbers, Calls, and Settings. The `CTM_TOKEN` and `CTM_SECRET` used above will determine which account(s) will be visible through the interface.


## Documentation

The reference documentation is found here: http://developers.calltrackingmetrics.com. Beta documentation using Postman can be found here: https://documenter.getpostman.com/view/213868/ctm-api/2FxGgg

### Accounts
Advanced or Enterprise CTM accounts can create any number of sub-accounts. To create a new account, you only need to provide an account name, timezone, and billing type. Currently, the only billing type allowed is `existing` which will place the account on agency billing.

### Numbers
If the account has tracking numbers, they will be listed along with their configuration. Numbers can be purchased for an account by clicking the `Buy Numbers` link at the right of the menu or at the right of the Numbers menu.

Before purchasing a number, you need to search for a number to purchase. In the United States (US) and Canada (CA), you can search by area code, address, pattern, or number to look for appropriate local numbers. For international numbers, searching is more restrictive because there is not good geocode data for international numbers.

After finding a number, you can purchase the number and add a name (also called a label or tracking_label.)

### Voice Menus
In voice messages, the parameter `play_message` can be either a `say` message or a `play` URL.

The format of a `say` message is as follows:

    say:{{voice}}:{{language}}:{{message}}

<table>
<thead>
<tr>
<th align="left">parameter</th>
  <th align="left">options</th>
  <th align="left">Language, Locale</th>
</tr>
</thead>
<tbody>
<tr>
    <td>{{voice}}</td>
    <td>`man` or `woman`</td/>
    </tr>
    <tr>
    <td>{{language}} if `{{voice}}` is `man` or `woman`</td>
    <td>en<br>
    en-gb<br>
    es<br>
    fr<br>
    de<br>
    </td>
    <td>
    English (US)<br>
    English (UK)<br>
    Spanish<br>
    French<br>
    German<br>
    </td>
</tr>
<tr>
  <td align="left">{{language}} if `voice` is `alice`</td>
  <td align="left">da-DK<br>
de-DE<br>
en-AU<br>
en-CA<br>
en-GB<br>
en-IN<br>
en-US<br>
ca-ES<br>
es-ES<br>
es-MX<br>
fi-FI<br>
fr-CA<br>
fr-FR<br>
it-IT<br>
ja-JP<br>
ko-KR<br>
nb-NO<br>
nl-NL<br>
pl-PL<br>
pt-BR<br>
pt-PT<br>
ru-RU<br>
sv-SE<br>
zh-CN<br>
zh-HK<br>
zh-TW<br></td>
<td align="left">
Danish, Denmark<br>
German, Germany<br>
English, Australia<br>
English, Canada<br>
English, UK<br>
English, India<br>
English, United States<br>
Catalan, Spain<br>
Spanish, Spain<br>
Spanish, Mexico<br>
Finnish, Finland<br>
French, Canada<br>
French, France<br>
Italian, Italy<br>
Japanese, Japan<br>
Korean, Korea<br>
Norwegian, Norway<br>
Dutch, Netherlands<br>
Polish-Poland<br>
Portuguese, Brazil<br>
Portuguese, Portugal<br>
Russian, Russia<br>
Swedish, Sweden<br>
Chinese (Mandarin)<br>
Chinese (Cantonese)<br>
Chinese (Taiwanese Mandarin)<br></td>
</tr>
</tbody>
</table>

The format of a play message is as follows:

    play:{{url}}

where `{{url}}` is the URL of an audio file in one of the following formats MP3, WAV, AIFF, GSM, μ-law and is smaller than 7MB, i.e.

    `play:http://www.springfieldfiles.com/sounds/homer/hacker.mp3`
