function setupSchedulePicker(defaultOptions) {
  if (!defaultOptions) { defaultOptions = {}; }
  var scheduleID = $("#schedule .picker").select2('val');
  console.log("scheduleID: ", scheduleID);
  if (!scheduleID || scheduleID == 'None') { $("#schedule_routing").hide(); return; }

  $("#schedule_routing").show();
  var objectType = $("#schedule_routing .route_select").select2('val');
  var template  = Mustache.to_html(Templates['route_to_' + objectType],defaultOptions);

  console.log("selected objectType: ", objectType);

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
});
