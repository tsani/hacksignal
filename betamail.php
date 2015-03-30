<html>
<head>
	<title></title>
</head>
<body>
	<?php 
	if(isset($_POST['submit'])){
	    $to = "hello@ariari.io"; // this is your Email address
	    $from = $_POST['email']; // this is the sender's Email address
	    $name = $_POST['name'];
	    $subject = "HackSignal Beta Interest";
	    $subject2 = "Copy of your form submission";
	    $message = $name . " wrote the following:" . "\n\n" . $_POST['event'];
	    $message2 = "Here is a copy of your message " . $name . "\n\n" . $_POST['date'];

	    $headers = "From:" . $from;
	    $headers2 = "From:" . $to;
	    mail($to,$subject,$message,$headers);
	    mail($from,$subject2,$message2,$headers2); // sends a copy of the message to the sender
	    echo "Mail Sent. Thank you " . $name . ", we will contact you shortly.";
	    // You can also use header('Location: thank_you.php'); to redirect to another page.
    }
	?>
</body>
</html>