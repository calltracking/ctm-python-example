function setupPicker(defaultOptions) {
  if (!defaultOptions) { defaultOptions = {}; }
  var objectType = $("#route_to select").select2('val');
  console.log(defaultOptions);
  var template   = Mustache.to_html(Templates['route_to_' + objectType],defaultOptions);
  console.log(template);

  $("#route_selection").html(template);

  $("#route_selection .picker").select2({
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
$(function() {
  
  $("#tracking_source select").select2({
    ajax: {
      url: "/lookup/tracking_source",
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
  $("#call_setting select").select2({
    ajax: {
      url: "/lookup/call_setting",
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

  $("#route_to select").select2().on("change", function() {
    var route = $(this).val();
    console.log("change to route:", route);
    setupPicker();
  });

  setupPicker({
    type: $("#route_selection").attr("data-type"),
    dial: $.grep($("#route_selection details").map(function() { 
      var id = $(this).attr("id");
      if (!id) { return null; }
      return {
        id: id,
        name: $(this).attr("name")
      }
    }).toArray(), function(n) { return n })
  });

});
