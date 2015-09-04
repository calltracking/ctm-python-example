var CartNumbers = [];
var ActiveOrderId = null;

function searchNumbers(e) { if (e) e.preventDefault();
  var country  = $(".search .country").val();
  var searchby = $(".search .searchby").val();
  var areacode = $(".search .areacode").val();

  $.get("/numbers/search/" + country + "/" + searchby, {areacode: areacode}, setupNumbersForPurchase);
}

function setupNumbersForPurchase(results) {
  $("#search-results").html(Mustache.to_html(Templates.search_numbers, results));
  $("#search-results .buy-number").click(addNumberToCart);
}

function addNumberToCart(e) { if (e) e.preventDefault();
  CartNumbers.push($(this).attr("data-number"));
  $(this).closest("li").remove();
  $("#cart").html(Mustache.to_html(Templates.cart, {numbers: CartNumbers}));
  $("#checkout").click(buyNumbersInCart);
}

function buyNumbersInCart(e) { if (e) e.preventDefault();
  $(".buy-numbers").hide();
  $("#search-results").html("");
  $("#cart").html("");
  $("#progress-status").html("Processing Your Order...");
  $.post("/numbers/buy", {"numbers[]": CartNumbers}, function(res) {
    console.log("buy response: ", res);
    ActiveOrderId = res.id;
  }).error(function(e) {
    ActiveOrderId = null;
    $("#progress-status").html("Error Processing Your Order. Please try again soon.");
  }).complete(function() {
    CartNumbers = []; // in case of error clear it out
    $(".buy-numbers").show();
  });
}

function purchaseEvent(msg) {
  console.log("purchaseEvent", msg);
  if (msg.id != ActiveOrderId) { return; }
  switch(msg.status) {
  case 'success':
    $("#progress-status").html("Order " + msg.message);
    break;
  case 'failure':
    $("#progress-status").html("Order " + msg.message);
  default:
    $("#progress-status").html("Purchased " + msg.purchased_count + " numbers");
    break;
  }

}

$(function() {
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/ctm');
  socket.on("linked", function(res) { console.log(res); });
  socket.on("purchase", purchaseEvent); // listen for purchaseEvent activity

  $(".buy-numbers").submit(searchNumbers);
  searchNumbers()
});
