var Templates = {
  route_to_voice_menu: '<label>Voice Menu</label>' +
    '<select class="picker" name="route_object" data-type="voice_menu">' +
    '  {{#dial}} ' +
      '<option value="{{id}}">{{name}}</option>' +
    '  {{/dial}} ' +
    '</select>',
  route_to_geo_config: '<label>Geo Router</label>' +
    '<select class="picker" name="route_object" data-type="geo_config">' +
    '  {{#dial}} ' +
      '<option value="{{id}}">{{name}}</option>' +
    '  {{/dial}} ' +
    '</select>',
  route_to_call_queue: '<label>Call Queue</label>' +
    '<select class="picker" name="route_object" data-type="call_queue">' +
    '  {{#dial}} ' +
    '    <option value="{{id}}">{{name}}</option> ' +
    '  {{/dial}} ' +
    '</select>',
  route_to_user: '<label>Call User/Agent</label>' +
    '<select class="picker" name="route_object" data-type="call_queue">' +
    '  {{#dial}} ' +
    '    <option value="{{id}}">{{name}}</option> ' +
    '  {{/dial}} ' +
    '</select>',
  route_to_receiving_number: '<label>Dial Multiple Numbers</label>' +
    '<select name="ringtype"><option>simultaneous</option><option>round robin</option></select>' + 
    '<select class="picker" name="route_object" multiple data-type="receiving_number">' +
    '  {{#dial}} ' +
    '    <option selected value="{{id}}">{{name}}</option> ' +
    '  {{/dial}} ' +
    '</select>',
}
