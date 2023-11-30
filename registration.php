<?php 
    
$showAlert = false;  
$showError = false;  
$exists=false; 
    
if($_SERVER["REQUEST_METHOD"] == "POST") { 
      
    // Include file which makes the 
    // Database Connection. 
    include 'db_connection.php';    

    $fname = $_POST["fname"];  
    $lname = $_POST["lname"];
    $email = $_POST["email"];
    $phnumber = $_POST["phnumber"]; 
    $password = $_POST["password"]; 
    $cpassword = $_POST["cpassword"]; 
            
    
    $sql = "Select * from user_details where email='$email'"; 
    
    $result = mysqli_query($conn, $sql); 
    
    $num = mysqli_num_rows($result);  

    // This sql query is use to check if 
    // the username is already present  
    // or not in our Database 
    if($num == 0) { 
        if(($password == $cpassword) && $exists==false) { 
    
            $hash = password_hash($password,  
                                PASSWORD_DEFAULT); 
            // Password Hashing is used here.  

            $sql = "INSERT INTO `user_details` (`first_name`,  
                `last_name`, `email`, `phone_number`, `password`) VALUES ('$fname',  
                '$lname', '$email', '$phnumber', '$hash')"; 
    
            $result = mysqli_query($conn, $sql); 
    
            if ($result) { 
                $showAlert = true;  
            } 
        }  
        else {  
            $showError = "Passwords do not match";  
        }       
    } else { 
      $exists="Email already used";  
    }  
    
}//end if    
    
?> 

<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LightXpense</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <link rel="stylesheet" href="css/style.css">

        <link rel="icon" type="image/png" href="image/logo2.png"/>
    </head>

    <body>

    <?php 
        
        if($showAlert) { 
            echo ' <div class="alert alert-success  
                alert-dismissible fade show" role="alert"> 
        
                <strong>Success!</strong> Your account is  
                now created and you can login.  
                <button type="button" class="close"
                    data-dismiss="alert" aria-label="Close">  
                    <span aria-hidden="true">×</span>  
                </button>  
            </div> ';  
        } 
        
        if($showError) { 
        
            echo ' <div class="alert alert-danger  
                alert-dismissible fade show" role="alert">  
            <strong>Error!</strong> '. $showError.'
        
        <button type="button" class="close" 
                data-dismiss="alert aria-label="Close"> 
                <span aria-hidden="true">×</span>  
        </button>  
        </div> ';  
    } 
            
        if($exists) { 
            echo ' <div class="alert alert-danger  
                alert-dismissible fade show" role="alert"> 
        
            <strong>Error!</strong> '. $exists.'
            <button type="button" class="close" 
                data-dismiss="alert" aria-label="Close">  
                <span aria-hidden="true">×</span>  
            </button> 
        </div> ';  
        } 
    
    ?> 

        <!--Start Header-->
        <div class="header">
            <div class="container">
                <img class="logo" src="image/logo.png" alt="" />
                <div class="links">
                    <div class="flex-links">
                        <ul class="nav-bar">
                            <li class="nav-item">
                                <a href="index.php">Home</a>
                            </li>
                            <li class="nav-item">
                                <a href="about.php">About</a>
                            </li>
                            <li class="nav-item">
                                <a href="claim.php">Claim Expenses</a>
                            </li>
                            <li class="nav-item">
                                <a href="dashboard.php">Dashboard</a>
                            </li>
                        </ul>
                        <div class="flex-icons">
                            <i class="fas fa-user"></i>
                            <ul class="user-menu">
                                <li>Hi, Guest!</li>
                                <li><a href="login.php">Login</a></li>
                                <li><a href="registration.php">Register</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- End Header -->

        <!-- Start Registration Page -->
        <div class = "registration">
            <div class = "container">
                <div class = "back">
                    <i class='fas fa-arrow-alt-circle-left' style="font-size: 100%; color: darkgray;"></i>
                    <a href="login.php">Back to Login</a>
                </div>
                <div class = "title">
                    <h1>Let's Get Started</h1>
                    <p>Welcome! Get started by creating your account:</p>
                </div>
                <form action="registration.php" method="post">
                <div class="name">
                    <div class="name-input">
                        <input type="text" placeholder="First Name" name="fname" required>
                        <i class="fa fa-user icon"></i>
                    </div>
                    <div class="name-input">
                        <input type="text" placeholder="Last Name" name="lname" required>
                        <i class="fa fa-user icon"></i>
                    </div>
                </div>
                <div class ="contact">
                    <div class="name-input">
                        <input type="text" placeholder="Email" name="email" required>
                        <i class="fa fa-envelope icon"></i>
                    </div>
                    <div class="name-input">
                        <input type="tel" placeholder="Phone Number" name="phnumber" required>
                        <i class="fa fa-phone icon"></i>
                    </div>
                    <div class="name-input">
                        <input type="password" placeholder="Create Password" name="password" required>
                        <i class="fas fa-lock"></i>
                    </div>
                    <div class="name-input">
                        <input type="password" placeholder="Confirm Password" name="cpassword" required>
                        <i class="fas fa-lock"></i>
                    </div>
                    <button type="submit" class="register-btn">REGISTER NOW</button>
                </div>
                </div>
            </form>

            </div>
        </div>

        <script src=" 
    https://code.jquery.com/jquery-3.5.1.slim.min.js" 
        integrity=" 
    sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" 
        crossorigin="anonymous"> 
    </script> 
        
    <script src=" 
    https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" 
        integrity= 
    "sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" 
        crossorigin="anonymous"> 
    </script> 
        
    <script src=" 
    https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"  
        integrity= 
    "sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
        crossorigin="anonymous"> 
    </script>  
    </body>
</html>