$("#logo").click(function() {
	$("body").addClass("light");
	$("#hidden").addClass("red");
	$("html, body").animate({scrollTop:600}, 1000);
});
