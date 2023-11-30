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

	<!--Start Status Bar-->
	<div class="status-bar">
		<div class="dot-green">
			<div class="dot-label">Claim</div>
		</div>
		<div class="line-green"></div>
		<div class="dot-green">
			<div class="dot-label">Confirmation</div>
		</div>
		<div class="line-grey"></div>
		<div class="dot-grey">
			<div class="dot-label">Dashboard</div>
		</div>
	</div>
	<!--End Status Bar-->
		
	<!-- Start Confirmation-->
		<div class="confirmation">
			<div class="image-container">
				<img class="image" src="image/receipt.png" data-img="">
			</div>
			<div class="details-container">
				<div class="details">
					<h3>Please confirm the details:</h3>
					<h6>* If the amount is correct, please click "Proceed", otherwise, please click "Upload Again"</h6>
					<div class="details-row">
						<label class="details-label">Expense Category</label>
						<input class="details-input" type="text" readonly value="Entertainment">
					</div>
					<div class="details-row">
						<label class="details-label">Amount</label>
						<input class="details-input" type="text" readonly value="RM57.65">
					</div>
				</div>
				<div class="buttons">
					<a href="#" class="button-process">Proceed</a>
					<a href="claim.php" class="button-upload">Upload Again</a>
			</div>
		</div>
	</div>
	</body>
	
</html>

