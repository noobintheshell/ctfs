<?php
session_start();

require_once("../inc/functions.inc.php"));

$error = null;

if ($_POST) {
    $pwd = get_password_by_name($_POST['user']);

    if ($_POST['username'] && !empty($_POST['username']) && $_POST['username'] === 'admin') {
        $error = 'Direct admin login not allowed';
    } else if ($_POST['password'] && !empty($_POST['password']) && strcmp($_POST['password'], $pwd) == 0) {
        
        $uid = get_uid_by_name($_POST['username']);
        $_SESSION['username'] = $_POST['username'];
        setcookie("uid", $uid);
        header('Location: protected.php');
        die();

    } else {
        $error = "Authentication Failed";
    }
}
?>

<html>
<head>
    <title>Query Explorer</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <style>
        body {
            background-color: #cacaca;
        }
        .container {
            margin-top: 50px;
        }
    </style>
</head>

<body>

    <div class="container">
        <h1>Login</h1>
        
        <?php
            if(isset($error)) {
                echo '<div class="alert alert-danger" role="alert">'.$error.'</div>';
            }
        ?>

        <div class="row">
            <div class="col-sm-12">
                <div class="card">
                  <div class="card-body">
                    <p class="card-text">
						<form method="post">
							<div class="form-group">
                                <label for="username">Username</label>
                                <input type="username" class="form-control" id="username" placeholder="Username" name="username">
								<label for="password">Password</label>
								<input type="password" class="form-control" id="password" placeholder="Password" name="password">
							</div>
							<button type="submit" class="btn btn-dark">Submit</button>
						</form>
                    </p>
                  </div>
                </div>
            </div>
        </div>
    </div>

</body>
</html>