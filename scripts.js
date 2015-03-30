$("#logo").click(function() {
	$("body").addClass("light");
	$("#hidden").addClass("red");
	$('html, body').animate({
        scrollTop: $('#section2')[0].scrollHeight
    }, 500);
});

$(".center-button").click(function() {
	$(".center-button").addClass("active");
	$(".left-button").removeClass("active");
	$(".right-button").removeClass("active");
});

$(".left-button").click(function() {
	$(".center-button").removeClass("active");
	$(".left-button").addClass("active");
	$(".right-button").removeClass("active");
});

$(".right-button").click(function() {
	$(".center-button").removeClass("active");
	$(".left-button").removeClass("active");
	$(".right-button").addClass("active");
});