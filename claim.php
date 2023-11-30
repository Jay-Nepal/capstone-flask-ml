<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Claim</title>
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    />
    <link rel="stylesheet" href="css/style.css" />
    
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

    
    <!--Start Status Bar-->
    <div class="status-bar">
	    <div class="dot-green">
		    <div class="dot-label">Claim</div>
	    </div>
	    <div class="line-grey"></div>
	    <div class="dot-grey">
		  <div class="dot-label">Confirmation</div>
	    </div>
	    <div class="line-grey"></div>
	    <div class="dot-grey">
		    <div class="dot-label">Dashboard</div>
	    </div>
    </div>
    <!--End Status Bar-->
     
  <!-- Start Claim Expenses -->
  <form action="">
    <div class="claim">
      <div class="container">
        <input type="file" id="file" accept="image/*" hidden>
        <div class="img-area">
          <h3>Upload Your Receipt</h3>
          <p>The file should be in <span>.png, .jpg, .jpeg, pdf</span></p>
          <i class="fas fa-solid fa-cloud-arrow-up"></i>
        </div>
        <div class="claim-buttons">
          <label for="file" class="select-image">Select Image</label>
          <a href="confirmation.php" class="submit">Submit</a>
        </div>
      </div>
    </div>
  </form>
  <!-- End Claim Expenses -->
  
  <script type="text/javascript" src="js/image_upload.js"></script>
  </body>
</html>
