$("#logo").click(function() {
	$("body").addClass("light");
	$("#hidden").addClass("red");
	$("html, body").animate({scrollTop:($("#section2")[0].scrollHeight)}, 1000);
});
