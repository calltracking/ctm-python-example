function routePicker(selector, objectType) {
  $(selector).select2({
    ajax: {
      url: "/lookup/" + objectType,
      dataType: 'json',
      delay: 250,
      data: function(params) {
        return {
          q: params.term,
          page: params.page
        }
      },
      processResults: function(data, page) {
        return data;
      },
      cache: true
    },
    minimumInputLength: 0
  });
}

function setupSchedulePicker(defaultOptions) {
  if (!defaultOptions) { defaultOptions = {}; }
  var scheduleID = $("#schedule .picker").select2('val');
  if (!scheduleID || scheduleID == 'None') { $("#schedule_routing").hide(); return; }

  $("#schedule_routing").show();
  var objectType = $("#schedule_routing .route_select").select2('val');
  var template  = Mustache.to_html(Templates['route_to_' + objectType],defaultOptions);

  $("#schedule_route_to").html(template);

  $("#schedule_route_to .picker").select2({
    ajax: {
      url: "/lookup/" + objectType,
      dataType: 'json',
      delay: 250,
      data: function(params) {
        console.log("lookup", params);
        return {
          q: params.term,
          page: params.page
        }
      },
      processResults: function(data, page) {
        console.log("processResults", data);
        return data;
      },
      cache: true
    },
    minimumInputLength: 0
  });
}

function loadItems() {
  var menu_id = $("#items").attr("data-id");
  $.get("/menus/" + menu_id + "/items", function(res) {
    console.log(res);
    $("#items").html(res.items.map(function(item) {
      return Mustache.to_html(Templates.menu_items[item.voice_action_type],item);
    }).join(""));
    $("#items .check-value").each(function() {
      var itemElement = $(this);
      var type        = itemElement.attr("data-type");
      var value       = itemElement.val();
      if (!value) { routePicker(itemElement, type); return; }
      var activeItem  = itemElement.find("option[value=" + value + "]");

      $.get("/lookup/" + type + "/" + value, function(res) {
        var opt = $("#items option[value=" + value + "]").get(0);
        opt.text = res.text;
        routePicker(itemElement, type);
      },'json');
    });
  });
}

$(function() {
  $("#schedule_routing .route_select").select2().on("change",setupSchedulePicker);

  $("#schedule .picker").select2({
    ajax: {
      url: "/lookup/" + "schedule",
      dataType: 'json',
      delay: 250,
      data: function(params) {
        console.log("lookup", params);
        return {
          q: params.term,
          page: params.page
        }
      },
      processResults: function(data, page) {
        console.log("processResults", data);
        return data;
      },
      cache: true
    },
    minimumInputLength: 0
  }).on("change", setupSchedulePicker);
  setupSchedulePicker();

  loadItems();
});
