$("#logo").click(function() {
	$("body").toggleClass("light");
	$("#hidden").toggleClass("red");
	$("html, body").animate({scrollTop:600}, 1000);
});
