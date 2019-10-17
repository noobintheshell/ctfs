<?php
  #ini_set('display_errors', 1);
  #ini_set('display_startup_errors', 1);
  #error_reporting(E_ALL);
  include('login.php'); // Includes Login Script
  if(isset($_SESSION['login_user'])){
    header("location: profile.php"); // Redirecting To Profile Page
  }
?>

<!DOCTYPE html>
<html>
	<head>
  		<title>ISMC - International Space Mission Center</title>
	<link href="style.css" rel="stylesheet" type="text/css">
	</head>
	<body>
		<div class="login-page">
  			<div class="form">
 				<div id="login" class=login-form>
					<img src=telescope.png width=100 height=100>
					<h2>International Space Mission Center</h2>
					<form action="" method="post">
						<input id="name" name="username" placeholder="username" type="text">
						<input id="password" name="password" placeholder="**********" type="password"><br>
						<button name="submit" type="submit">Login</button>
						<span class="message"><?php echo $error; ?></span>
						<p class=message><a href="forgot.php">Forgot Password</a></p>
					</form>
				</div>
			</div>
 		</div>
	</body>
</html>
