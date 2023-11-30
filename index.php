<?php
include 'db_connection.php';
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

<!-- Start Welcome-->
  <div class="welcome">
    <div class="container">
        <div class="detail-box">
            <h2>Welcome to</h2>
            <h1>LightXpense</h1>
            <p>You can effortlessly claim your expenses in just one go by snapping a photo of your receipt</p>
            <div class="start-button">
            <a href="claim.php">Claim Now</a>
            </div>
        </div>
    </div>
  </div>
<!--End Welcome-->

<!-- Start Services-->
  <div class="do_section">
    <div class="intro-text">
      <h2>- Services -</h2>
    </div>
    <div class="features">
        <div class="container">
          <div class="feat">
            <i class="fas fa-solid fa-camera"></i>
            <h3>Snap & Claim</h3>
            <p>Say goodbye to manual data entry! LightXpense allows employees to effortlessly claim expenses by simply snapping a photo of their receipts.</p>
          </div>
          <div class="feat">
            <i class="fas fa-globe-americas"></i>
            <h3>Access Anytime, Anywhere</h3>
            <p>Need to submit a claim on the go? No problem! Our mobile-friendly platform lets you submit expenses from anywhere, at any time.</p>
          </div>
          <div class="feat">
            <i class="fas fa-solid fa-chart-column"></i>
            <h3>Tracking</h3>
            <p>LightXpense provides updates on the status of your claims, giving you peace of mind and transparency into the entire process.</p>
          </div>
          <div class="feat">
            <i class="fa fa-area-chart"></i>
            <h3>Analytics</h3>
            <p>Through intuitive dashboards, our platform enables users to identify trends, assess risk factors, and make informed decisions with precision.</p>
          </div>
        </div>
      </div>
  </div>
<!--End Services->

</body>
