<?php

include 'db_connection.php';

if(isset($_POST['submit'])){
   $firstName = mysqli_real_escape_string($conn, $_POST['firstName']);
   $lastName = mysqli_real_escape_string($conn, $_POST['lastName']);
   $email = mysqli_real_escape_string($conn, $_POST['email']);
   $phone = mysqli_real_escape_string($conn, ($_POST['phone']));   
   $password = mysqli_real_escape_string($conn, ($_POST['password']));
   $department = mysqli_real_escape_string($conn, ($_POST['department']));

   $select_users = mysqli_query($conn, "SELECT * FROM `user_details` WHERE email = '$email' AND password = '$password'") or die('query failed');

   if(mysqli_num_rows($select_users) > 0){
        $error_message = 'User already exists!';
   }else{
        mysqli_query($conn, "INSERT INTO `user_details`(first_name, last_name, email, phone_number, password, department) VALUES ('$firstName', '$lastName', '$email', '$phone', '$password', '$department')") or die('query failed');
        $success_message = 'Registered successfully!';
   }
}

?>

<style> 
        .container {
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: 30rem;
        }

        .container form label {
            display: block;
            margin-bottom: 8px;
        }

        .container form input {
            width: 100%;
            padding: 8px;
            margin-bottom: 16px;
            box-sizing: border-box;
        }

        button {
            background-color: #4caf50;
            color: #fff;
            padding: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            display: block;
            width: 60%;
            margin: 0 auto;
        }

        button:hover {
            background-color: #45a049;
        }

        /* Style for error or success message */
        .message-container {
            margin-top: 20px;
        }

        .message {
            position: relative;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 10px;
        }

        .error-message {
            background-color: #f44336;
            color: white;
        }

        .success-message {
            background-color: #4caf50;
            color: white;
        }

        .close-button {
            position: absolute;
            top: 5px;
            right: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
</style>

<!-- Display Error or Success Message -->
<div class="message-container">
    <?php
    if(isset($error_message)){
        echo '
        <div class="message error-message">
            <span>'.$error_message.'</span>
            <i class="fas fa-times close-button" onclick="this.parentElement.remove();"></i>
        </div>
        ';
    }

    if(isset($success_message)){
        echo '
        <div class="message success-message">
            <span>'.$success_message.'</span>
            <i class="fas fa-times close-button" onclick="this.parentElement.remove();"></i>
        </div>
        ';
    }
    ?>
</div>

<div class="container">
<form method="post">
        <label for="firstName">First Name:</label>
        <input type="text" id="firstName" name="firstName" required>

        <label for="lastName">Last Name:</label>
        <input type="text" id="lastName" name="lastName" required>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required>

        <label for="phone">Phone Number:</label>
        <input type="tel" id="phone" name="phone" required>

        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>

        <label for="department">Department:</label>
        <input type="text" id="department" name="department" required>

        <button type="submit" name="submit">Register</button>
</form>
</div>
