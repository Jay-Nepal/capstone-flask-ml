<?php
if (isset($_POST['submit'])) {
    $uploadDir = 'uploads/'; // Directory to store uploaded images
    $uploadFile = $uploadDir . basename($_FILES['image']['name']);
    
    // Check if the file is an image
    $imageFileType = strtolower(pathinfo($uploadFile, PATHINFO_EXTENSION));
    $allowedExtensions = ['jpg', 'jpeg', 'png', 'gif'];

    if (in_array($imageFileType, $allowedExtensions)) {
        if (move_uploaded_file($_FILES['image']['tmp_name'], $uploadFile)) {
            echo 'Image has been uploaded successfully.';
        } else {
            echo 'Error uploading image.';
        }
    } else {
        echo 'Invalid file format. Please upload a valid image (jpg, jpeg, png, gif).';
    }
}
?>
