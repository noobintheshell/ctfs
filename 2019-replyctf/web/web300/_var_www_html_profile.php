<?php
include('session.php');
if(!isset($_SESSION['login_user'])){
  header("location: index.php"); // Redirecting To Home Page
  die('Nope');
}
?>
<!DOCTYPE html>
<html>
<head>
 <title>Kepler Status Board</title>
 <link href="style.css" rel="stylesheet" type="text/css">
</head>
<body>
 <div id="profile" class="profile-page">
 <b id="welcome">Welcome <i><?php echo $_SESSION['login_user']; ?></i></b>
 <br/>
<p>This is the latest image our satellite telescope captured from Mars. Next image transfer will finish in <i>42 hours</i>.</p>
 <br/>
<img src="Mars(actually-captured-by-Hubble).png" title="VGhpcyBpcyBub3QgdGhlIGZsYWcgeW91IGFyZSBsb29raW5nIGZvcjop">
<br/><br><br>
<button id="logout"><p class=message><a href="logout.php">Log Out</a></p></button>
 </div>
</body>
</html>
