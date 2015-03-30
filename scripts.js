$("#logo").click(function() {
	$("body").addClass("light");
	$("#hidden").addClass("red");
	$('html, body').animate({
        scrollTop:$('#section2')[0].scrollHeight
    }, 500);
    $("#logo").css("cursor", "default");
});

$(window).scroll(function() {
  	$("body").addClass("light");
	$("#hidden").addClass("red");
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
	$("#beta-full, #beta-full *, #pop-up-overlay").show(500);
	event.preventDefault(); 
	$("#full-email").val($("#interest-email").val());
});

$("#pop-up-overlay").click(function() {
	$("#beta-full, #pop-up-overlay").hide(500);
});

$("#beta-full").submit(function(event) {
	event.preventDefault(); 
	Parse.initialize("VZnzhx2yDi4XARcEY8FrT7cYzJPRdG9UJNwA4Xef", "z8ULgqRkygDY5uUvClqZhay5FOnwXrdBnnanK3xg");
	var betaUser = Parse.Object.extend("BetaInterest");
	var betaUser = new betaUser();
	betaUser.set({
		"name": $("input[name='name']").val(),
		"email": $("input[name='email']").val(),
		"event": $("input[name='event']").val(),
		"date": $("input[name='date']").val(),
		"website": $("input[name='site']").val(),
		"hackers": $("input[name='hackers']").val(),
	});
	betaUser.save().then(function(object) {
	  alert("Thank you for your interest! The HackSignal team will be in touch soon.");
	});
	$("#beta-full, #pop-up-overlay").hide(500);
});