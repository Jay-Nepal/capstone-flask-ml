<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login</title>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    />
    <link rel="stylesheet" href="style1.css" />
  </head>

  <body>
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

    <!-- Start Login Page-->
    <div class="login">
      <div class="container">
        <div class="title">
          <h1>User Login</h1>
          <i class="fas fa-user-circle"></i>
        </div>
        <div class="text-input">
          <input type="number" placeholder="Enter User ID" />
          <i
            class="fas fa-id-card-alt"
            style="font-size: 100%; color: darkgray"
          ></i>
        </div>
        <div class="text-input">
          <input type="password" placeholder="Enter Password" />
          <i
            class="fas fa-user-lock"
            style="font-size: 100%; color: darkgray"
          ></i>
        </div>
        <a href="index.php" class="login-btn">LOGIN</a>
        <div class="forgot">
          <a href="#" class="forgot">Forgot Username/Password?</a>
        </div>
        <div class="create">
          <a href="registration.php">Create Your Account</a>
          <i
            class="fas fa-arrow-alt-circle-right"
            style="font-size: 100%; color: darkgray"
          ></i>
        </div>
      </div>
    </div>
  </body>
</html>
