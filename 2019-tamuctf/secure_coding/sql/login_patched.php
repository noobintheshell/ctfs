<?php
  ini_set('display_errors', 'Off');
  error_reporting(0);
  echo "<html>";
  if (isset($_POST["username"]) && isset($_POST["password"])) {
    $servername = "localhost";
    $username = "sqli-user";
    $password = 'AxU3a9w-azMC7LKzxrVJ^tu5qnM_98Eb';
    $dbname = "SqliDB";
    $conn = new mysqli($servername, $username, $password, $dbname);
    if ($conn->connect_error)
        die("Connection failed: " . $conn->connect_error);
    $user = $_POST['username'];
    $pass = $_POST['password'];
    $sql = "SELECT * FROM login WHERE User=? AND Password=?";
    if ($stmt = $conn->prepare($sql))
    {
      $stmt->bind_param("ss", $user, $pass);
      $stmt->execute();
      $result = $stmt->get_result();
      if ($result->num_rows >= 1)
      {
        $row = $result->fetch_assoc(); 
        echo "You logged in as " . $row["User"];
        $row = $result->fetch_assoc();
        echo "<html>You logged in as " . $row["User"] . "</html>\n";
      }
      else {
        echo "Sorry to say, that's invalid login info!";
      }
    }
    $stmt->close();
    $conn->close();
  }
  else
    echo "Must supply username and password...";
  echo "</html>";
?>
