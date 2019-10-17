<link href="style.css"rel="stylesheet"type="text/css">
<?php 
    $fertig=$_POST["fertig"];
    $benutzername=$_POST["benutzername"];
    $rc=0;
    $conn=new mysqli("localhost","admin","pass","company");
    
    if($conn->connect_error)
    {
        die("ERROR: Unable to connect: ".$conn->connect_error);
    }
    echo "<div id=content class=\"login-page\">";
    
    forgot($fertig,$benutzername,$rc);echo "</div>";
    
    function forgot($fertig,$benutzername,$rc)
    {
        if($fertig)
        {
            $fertig="";
            $conn=new mysqli("localhost","admin","pass","company");
            $benutzername=addslashes($benutzername);
            mysqli_query($conn,"SET CHARACTER SET GBK");
            $result=mysqli_query($conn,"SELECT username,AES_DECRYPT(password,'V3ryNic3K3yToR3c3iv3Y0urFl4g') FROM safelogin WHERE username='$benutzername'");
            if($benutzername=="")
            {
                $rc=1;
                forgot($fertig,$benutzername,$rc);
            }
            else if(mysqli_num_rows($result)>0)
            {
                $row=mysqli_fetch_object($result);
                echo($nachricht);$rc=3;$benutzername="";
                forgot($fertig,$benutzername,$rc);
            }
            else
            {
                $rc=2;
                forgot($fertig,$benutzername,$rc);
            }
        }
        else
        {
            echo "<html><head><title>Forgot my Password</title><link rel=stylesheet href=\"css/style.css\"></head><body>";
            echo '<div id="login" align=center>';
            echo '<div class="login-page"><div class="form">';
            echo "<div id=title><img src=lost.png width=100 height=100><h2>Forgot Password<h2></div>";
            echo "<form method=post action=\"forgot.php?action=1\">";
            echo"<input id=benutzeri type=text name=benutzername class=login-form placeholder='username' value=".htmlspecialchars($benutzername).">";
            echo "<br><button type=submit value=\"Send\" class=button>Send</button><input type=hidden name=fertig value=yes>";
            
            switch($rc)
            {
                case 1:
                    echo "<div class=message> No Username provided.</div>";
                    break;
                case 2:
                    echo "<div class=message> Username does not exist.</div>";
                    break;
                case 3:
                    echo "<div class=message> The Password has been sent to you.</div>";
                    break;
            }
            unset($rc);
            echo "<p align=center class=message><a href=index.php>Back</a></p></form></div></div></body></html>";
        }
    } 
?>