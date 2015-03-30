$("#logo").click(function() {
	$("body").addClass("light");
	$("#hidden").addClass("red");
	$('html, body').animate({
        scrollTop:$('#section2')[0].scrollHeight
    }, 500);
    $("#logo").css("cursor", "default");
});

$("#section3").click(function() {
	$('html, body').animate({
        scrollTop:$('#section4').offset().top
    }, 500);
});

$(".center-button").click(function() {
	$(".center-button").addClass("active");
	$(".left-button").removeClass("active");
	$(".right-button").removeClass("active");
	$("#screenshot1").hide();
	$("#screenshot2").show();
	$("#screenshot3").hide();
});

$(".left-button").click(function() {
	$(".center-button").removeClass("active");
	$(".left-button").addClass("active");
	$(".right-button").removeClass("active");
	$("#screenshot1").show();
	$("#screenshot2").hide();
	$("#screenshot3").hide();
});

$(".right-button").click(function() {
	$(".center-button").removeClass("active");
	$(".left-button").removeClass("active");
	$(".right-button").addClass("active");
	$("#screenshot1").hide();
	$("#screenshot2").hide();
	$("#screenshot3").show();
});

$("#beta-interest").submit(function(event) {
	$("#beta-full, #beta-full *, #pop-up-overlay").show();
	event.preventDefault(); 
	$("#full-email").val($("#interest-email").val());
});

$("#pop-up-overlay").click(function() {
	$("#beta-full, #pop-up-overlay").hide();
});