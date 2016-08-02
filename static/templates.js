var RouteTemplates = {
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
    '<select class="picker" name="route_object[]" multiple data-type="receiving_number">' +
    '  {{#dial}} ' +
    '    <option selected value="{{id}}">{{name}}</option> ' +
    '  {{/dial}} ' +
    '</select>'
};
var TagTemplate = '<select multiple="multiple" class="tagpicker">{{#tag_list}}<option>{{.}}</option>{{/tag_list}}</select>';
var AgentTemplate = '<select class="agentpicker">{{#assign_agent_id}}<option value="{{assign_agent_id}}></option>{{/assign_agent_id}}</select>';
var MenuFooter = '<footer class="footer">' +
                    '<div><label>KeyPress</label> <input type="text" size="3" name="keypress" value="{{keypress}}"/></div>' +
                    '<div><label>Tag</label> ' + TagTemplate + '</div>' +
                    '<div><label>Agent</label> ' + AgentTemplate + '</div></footer>';
var Templates = {
  search_numbers: '{{#numbers}}<li>{{phone_number}} <a class="buy-number" href="#add" data-number={{phone_number}}>add</a></li>{{/numbers}}',
  cart: '<h3>Order Numbers <a id="checkout" href="#checkout">Buy Numbers</a></h3><ul>{{#numbers}}<li data-number="{{.}}">{{.}}</li>{{/numbers}}</ul>',

  menu_items: {
    dial: '<section class="item"><h3>Dial Number</h3>' + 
            '<label>Play Message Before Dialing</label><input type="text" name="items[play_message]" value="{{play_message}}"/><p></p>' +
            '<label>Whisper to answering party</label><input type="text" name="items[whisper_message]" value="{{whisper_message}}"/><p></p>' +
            '<label>Dial Number</label><select class="check-value" data-type="receiving_number" name="items[physical_phone_number_id]"><option value="{{physical_phone_number_id}}"></option></select><p></p>' +
            MenuFooter +
          '</section>',
    configured: '<section class="item"><h3>Pass through</h3>' +
                MenuFooter +
                '</section>',
    menu: '<section class="item"><h3>Next Menu</h3>' +
          MenuFooter +
          '</section>',
    sms: '<section class="item"><h3>Send Message</h3>' +
          MenuFooter +
         '</section>',
    collect_input: '<section class="item"><h3>Collect Menu Input</h3>' +
                    MenuFooter +
                   '</section>',
    fire_pixel: '<section class="item"><h3>Trigger a pixel request</h3>' +
                    MenuFooter +
                '</section>',
    call_agent: '<section class="item"><h3>Dial an Agent</h3>' +
                    MenuFooter +
                '</section>',
    message: '<section class="item"><h3>Record a message</h3>' +
                    MenuFooter +
             '</section>',
    conference: '<section class="item"><h3>Join a conference call</h3>' +
                    MenuFooter +
                '</section>',
    hangup: '<section class="item"><h3>Hangup the call</h3>' +
                    MenuFooter +
            '</section>',
    call_queue: '<section class="item"><h3>Enter a Queue</h3>' +
                    MenuFooter +
                '</section>',
    geo: '<section class="item"><h3>Geo Route</h3>' +
                    MenuFooter +
         '</section>',
    conditional_router: '<section class="item"><h3>Choose Conditional Router</h3>' +
                    MenuFooter +
                        '</section>'
  }
}
Object.keys(RouteTemplates).forEach(function(key) {
  Templates[key] = RouteTemplates[key];
});
