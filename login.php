<?php

include 'db_connection.php';

session_start();

if(isset($_POST['submit'])){

   $email = mysqli_real_escape_string($conn, $_POST['email']);
   $pass = mysqli_real_escape_string($conn, ($_POST['pass']));

   $select_users = mysqli_query($conn, "SELECT * FROM `user_details` WHERE email = '$email' AND password = '$pass'") or die('query failed');

   if(mysqli_num_rows($select_users) > 0){

      $row = mysqli_fetch_assoc($select_users);

      $_SESSION['name'] = $row['first_name'];
      $_SESSION['email'] = $row['email'];
      $_SESSION['department'] = $row['department'];

      if($row['department'] == 'ADMIN'){
    
         header('location:admin.php?module=dashboard&page=admin');

      }else{
        
         header('location:user.php?module=dashboard&page=home');

      }

   } else{
      $errors[] = 'Incorrect email or password';
   }

}

?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <title>LightXpense</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <!--===============================================================================================-->
    <link rel="shortcut icon" href="images/logo2.png" type="image/png" />
    <!--===============================================================================================-->
    <link
      rel="stylesheet"
      type="text/css"
      href="vendor/bootstrap/css/bootstrap.min.css"
    />
    <!--===============================================================================================-->
    <link
      rel="stylesheet"
      type="text/css"
      href="fonts/font-awesome-4.7.0/css/font-awesome.min.css"
    />
    <!--===============================================================================================-->
    <link
      rel="stylesheet"
      type="text/css"
      href="fonts/iconic/css/material-design-iconic-font.min.css"
    />
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="vendor/animate/animate.css" />
    <!--===============================================================================================-->
    <link
      rel="stylesheet"
      type="text/css"
      href="vendor/css-hamburgers/hamburgers.min.css"
    />
    <!--===============================================================================================-->
    <link
      rel="stylesheet"
      type="text/css"
      href="vendor/animsition/css/animsition.min.css"
    />
    <!--===============================================================================================-->
    <link
      rel="stylesheet"
      type="text/css"
      href="vendor/select2/select2.min.css"
    />
    <!--===============================================================================================-->
    <link
      rel="stylesheet"
      type="text/css"
      href="vendor/daterangepicker/daterangepicker.css"
    />
    <!--===============================================================================================-->
    <link rel="stylesheet" type="text/css" href="css/util.css" />
    <link rel="stylesheet" type="text/css" href="css/login.css" />
    <!--===============================================================================================-->
  </head>
  <body>
    
  <header id="header">
      <div class="header-logo">
        <a href="index.php">LightXpense</a>
      </div>

      <nav id="header-nav-wrap">
        <ul class="header-main-nav">
          <li>
            <a href="index.php" title="home">Return Home</a>
          </li>
          <li><a href="mailto:aarogya@banepali.com" title="about">Contact Support</a></li>
      </nav>

      <a class="header-menu-toggle" href="#"><span>Menu</span></a>
    </header>
  
    <!-- /header -->

    <div class="limiter">
      <div class="container-login100">
        <div class="wrap-login100">
          <form class="login100-form validate-form" method="POST">
            <span class="login100-form-title p-b-26"> LightXpense login </span>

            <div
              class="wrap-input100 validate-input"
              data-validate="Valid email is: a@b.c"
            >
              <input class="input100" type="text" name="email" />
              <span class="focus-input100" data-placeholder="Email"></span>
            </div>

            <div
              class="wrap-input100 validate-input"
              data-validate="Enter password"
            >
              <span class="btn-show-pass">
                <i class="zmdi zmdi-eye"></i>
              </span>
              <input class="input100" type="password" name="pass" />
              <span class="focus-input100" data-placeholder="Password"></span>
            </div>

            <div class="container-login100-form-btn" style="margin-bottom:1rem">
              <div class="wrap-login100-form-btn">
                <div class="login100-form-bgbtn"></div>
                <button class="login100-form-btn" type="submit" name="submit">Login</button>
              </div>
            </div>
                      <!-- Error Message Display -->
                      <?php if (!empty($errors)): ?>
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                          </button>
                          <?php foreach ($errors as $error): ?>
                            <strong>Error <br></strong> <?php echo $error; ?><br>
                          <?php endforeach; ?>
                        </div>
                      <?php endif; ?>

            <div class="text-center p-t-50">
              <span class="txt1">
                Reach your workspace admin for issues <br>
              </span>

              <a class="txt2" href="mailto:aarogya@banepali.com"> Or contact our support</a>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div id="dropDownSelect1"></div>

    <!--===============================================================================================-->
    <script src="vendor/jquery/jquery-3.2.1.min.js"></script>
    <!--===============================================================================================-->
    <script src="vendor/animsition/js/animsition.min.js"></script>
    <!--===============================================================================================-->
    <script src="vendor/bootstrap/js/popper.js"></script>
    <script src="vendor/bootstrap/js/bootstrap.min.js"></script>
    <!--===============================================================================================-->
    <script src="vendor/select2/select2.min.js"></script>
    <!--===============================================================================================-->
    <script src="vendor/daterangepicker/moment.min.js"></script>
    <script src="vendor/daterangepicker/daterangepicker.js"></script>
    <!--===============================================================================================-->
    <script src="vendor/countdowntime/countdowntime.js"></script>
    <!--===============================================================================================-->
    <script src="js/login.js"></script>
  </body>
</html>
