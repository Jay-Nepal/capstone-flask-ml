<?php

include 'db_connection.php';

if(isset($_SESSION['email'])){
    $email = $_SESSION['email'];
  }

if (isset($_GET['status'])) {
    // Decode variables from URL
    $message = urldecode($_GET['status']);
    $category = urldecode($_GET['label']);
    $amount = urldecode($_GET['total']);
    $claimed_date = urldecode($_GET['date']);
}

?>

<style>

* {
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
}

:root {
  --dark-green: #006400;
  --light-green: #20b2aa;
  --light-grey: #f2f2f2;
}

html {
  scroll-behavior: smooth;
}

body {
  background-image: url("image/Web.png");
  background-size: cover;
}

html,
body {
  max-width: 100%;
  overflow-x: hidden;
}

.container {
  padding-left: 15px;
  padding-right: 15px;
  margin-left: auto;
  margin-right: auto;
}

  /* start claim status bar*/
.status-bar {
  display: flex;
  align-items: center;
  margin: 50px auto;
  width: 45%;
  justify-content: space-between;
}

.dot-green,
.dot-grey {
  position: relative;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin: 0 5px;
}

.dot-green {
  background: var(--light-green);
}

.dot-grey {
  background-color: #ccc;
}

.line-grey,
.line-green {
  height: 2px;
  background-color: #ccc;
  width: 200px;
  margin: 0 5px;
}

.line-green {
  background: var(--light-green);
}

.dot-label {
  position: absolute;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 11px;
  color: #333;
}
/* end claim status bar*/

/* start claim */
.claim .container {
  max-width: 400px;
  width: 100%;
  background-color: #ededed;
  padding: 30px;
  border-radius: 30px;
  margin-top: 10vh;
}

.img-area {
  position: relative;
  width: 100%;
  height: 26rem;
  background-color: rgb(209, 207, 207);
  margin-bottom: 30px;
  border-radius: 15px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.img-area i {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 200px;
  color: rgba(255, 255, 255, 0.5);
  z-index: 1;
}

.img-area img {
  width: 100%;
  height: 100%;
  object-fit: scale-down;
}

.img-area h3 {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 6px;
  z-index: 2;
}

.img-area p {
  color: #999;
  z-index: 2;
}

.img-area p span {
  font-weight: 600;
  z-index: 2;
}

.select-image {
  display: block;
  width: 100%;
  padding: 16px 0;
  border-radius: 15px;
  background: var(--light-green);
  color: #fff;
  font-weight: 500;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 10px;
  text-align: center;
  text-decoration: none;
}

.select-image:hover {
  background: var(--dark-green);
}

.submit {
  display: block;
  width: 100%;
  padding: 16px 0;
  border-radius: 15px;
  background: var(--light-green);
  color: #fff;
  font-weight: 500;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  text-decoration: none;
}

.submit:hover {
  background: var(--dark-green);
}
/* end claim */

/* start confirmation */
.confirmation {
  display: flex;
}

.image-container {
  width: 50%;
  text-align: center;
  position: relative;
  margin: 25px;
}

.image {
  position: relative;
  width: 80%;
  height: 75vh;
  background: var(--light-grey);
  border-radius: 15px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  margin: 0 auto;
}

.details-container {
  width: 50%;
  margin: 25px;
}

.details {
  margin: 0px;
}

.details h6 {
  margin: 0;
}

.details-row {
  display: flex;
  flex-direction: column;
}

.details-label {
  font-weight: bold;
  font-size: 15px;
  margin: 0;
}

.details-input {
  padding: 10px;
  border: 1px solid #ccc;
  width: 65%;
  height: 45px;
  background: var(--light-grey);
  color: #333;
}

.buttons {
  display: flex;
  justify-content: left;
  align-items: center;
  margin-top: 40px;
}

.button-process,
.button-upload {
  width: 30%;
  margin-right: 35px;
  padding: 15px 0;
  border-radius: 15px;
  font-weight: 500;
  font-size: 16px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  text-decoration: none;
  background: var(--light-green);
  color: #fff;
}

.button-process:hover,
.button-upload:hover {
  background: var(--dark-green);
}

body {
  font-family: Arial, sans-serif;
  background-color: #f2f2f2;
  margin: 0;
  padding: 0;
}

.claim-details-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.claim-details {
  margin-bottom: 20px;
}

h2 {
  color: #333;
}

p {
  margin: 10px 0;
}

.buttons-container {
  display: flex;
  justify-content: space-between;
}

.dashboard-button,
.all-claims-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  text-decoration: none;
  color: #fff;
  cursor: pointer;
}

.dashboard-button {
  background-color: #20b2aa;
}

.all-claims-button {
  background-color: #006400;
}

.dashboard-button:hover,
.all-claims-button:hover {
  opacity: 0.8;
}

/* end confirmation*/

</style>

<!--Start Status Bar-->
<div class="status-bar">
		<div class="dot-green">
			<div class="dot-label">Claim</div>
		</div>
		<div class="line-green"></div>
		<div class="dot-green">
			<div class="dot-label">Confirmation</div>
		</div>
		<div class="line-green"></div>
		<div class="dot-green">
			<div class="dot-label">Submit</div>
		</div>
</div>

<div class="claim-details-container">
    <div class="claim-details">
      <h2>Claim Details</h2>
      <p><strong>Amount:</strong> <?php echo $amount; ?></p>
      <p><strong>Category:</strong> <?php echo $category; ?></p>
      <p><strong>Date:</strong> <?php echo $claimed_date; ?></p>
      <p><strong>Message:</strong> <?php echo $message; ?></p>
    </div>

    <div class="buttons-container">
      <a href="user.php?module=dashboard&page=home" class="dashboard-button">Go to Dashboard</a>
      <a href="user.php?module=See%20Your%20Claims&page=claims" class="all-claims-button">See all Claims</a>
    </div>
  </div>