<?php
session_start();

if (!isset($_SESSION['username'])) {
	header('Location: index.php');
    die();
}

$uid = $_COOKIE['uid'];
$error = null;

if ($uid == "1" && $_SESSION['username'] !== 'admin') {
    $error = "Only admin user is allowed to have uid 1";
}

if (intval($uid) !== 1) {
    $error = "Only admin user is allowed to use this function";
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

<?php
    if(isset($error)) {
        echo '<div class="alert alert-danger" role="alert">'.$error.'</div>';
    } else {
    	// TODO
    }
?>

</body>
</html>