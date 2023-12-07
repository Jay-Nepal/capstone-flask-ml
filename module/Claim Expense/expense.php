<?php

if (isset($_POST['submit'])) {
  $uploadDir = 'uploads/'; // Directory to store uploaded images
  $uploadName = basename($_FILES['image']['name']);
  $uploadFile = $uploadDir . basename($_FILES['image']['name']);
  $file_path = urlencode($uploadFile);
  // Check if the file is an image
  $imageFileType = strtolower(pathinfo($uploadFile, PATHINFO_EXTENSION));
  $allowedExtensions = ['jpg', 'jpeg', 'png', 'gif'];

  if (in_array($imageFileType, $allowedExtensions)) {
      if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadFile)) {

          // Call Python script with the uploaded file name
          $pythonScript = 'uploads/main.py'; // Replace with the actual path to your Python script          
          // Execute the command
          $output = shell_exec("python $pythonScript $uploadName 2>&1");
          
          // Decode the JSON-like string into a PHP array
          $data = json_decode($output, true);

          if ($data === null || json_last_error() !== JSON_ERROR_NONE) {
            // Display an error div with a close button
            $error_message = "Failed to decode JSON string. Error: " . json_last_error_msg();
            include('error_message.php'); // Include a separate file for error message display
          } else {
            $status = $data['status'];
            $label = $data['label'];
            $category = urlencode($label);
            $amount = $data['amount'];
            $totalamount = urldecode($amount);

            if ($status === 400) {
              // Display an error div with a close button
              $error_message = "The receipt you uploaded isn't in MYR";
              include('error_message.php'); // Include a separate file for error message display
            } else {
              header("Location: user.php?module=Claim%20Expense&page=confirm&file_name=$file_path&category=$category&totalamount=$totalamount");
            }
          }
      } else {
          // Display an error div with a close button
          $error_message = 'Error uploading image.';
          include('error_message.php'); // Include a separate file for error message display
      }
  } else {
      // Display an error div with a close button
      $error_message = 'Invalid file format. Please upload a valid image (jpg, jpeg, png, gif).';
      include('error_message.php'); // Include a separate file for error message display
  }
}

?>


<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

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
  height: 240px;
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
  margin: 10px;
}

.details h6 {
  padding-bottom: 20px;
}

.details-row {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.details-label {
  font-weight: bold;
  margin-bottom: 20px;
  font-size: 15px;
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

/* end confirmation*/

</style>

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
		    <div class="dot-label">Submit</div>
	    </div>
    </div>
    <!--End Status Bar-->
     
  <!-- Start Claim Expenses -->
  <form method="post" enctype="multipart/form-data">
    <div class="claim">
      <div class="container">
        <input type="file" name="image" id="file" accept="image/*" hidden>
        <div class="img-area">
          <h3>Upload Your Receipt</h3>
          <p>The file should be in <span>.png, .jpg, .jpeg, pdf</span></p>
          <i class="fas fa-solid fa-cloud-arrow-up"></i>
        </div>
        <div class="claim-buttons">
          <label for="file" class="select-image">Select Image</label>
          <input type="submit" value="Upload Image" name="submit" class="select-image">
        </div>
      </div>
    </div>
  </form>
  <!-- End Claim Expenses -->
  
  <script type="text/javascript" src="js/image_upload.js"></script>