<style>
                .edit_form {
                    max-width: 600px;
                    margin: 0 auto;
                }

                .edit_label {
                    display: block;
                    margin-bottom: 10px;
                }

                .edit_input {
                    width: 100%;
                    padding: 8px;
                    margin-bottom: 15px;
                    box-sizing: border-box;
                }

                .edit_button {
                    padding: 10px;
                }
</style>

<?php
// edit_page.php

// Check if the ID parameter is set in the URL
if (isset($_GET['id'])) {
    $id = $_GET['id'];

    // Perform database connection and retrieve data based on ID
    $db = new myConnection();
    $sql = "SELECT * FROM chart_data WHERE id = '$id'";
    $result = $db->query($sql);

    if ($result->num_rows == 1) {
        $row = $result->fetch_assoc();

        // Check if the form is submitted for updates
        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['save'])) {
            // Retrieve updated values from the form
            $updatedDate = $_POST['updated_date'];
            $updatedMonth = $_POST['updated_month'];
            $updatedCategory = $_POST['updated_category'];
            $updatedAmount = $_POST['updated_amount'];

            // Update the data in the database
            $updateSql = "UPDATE chart_data SET date = '$updatedDate', month = '$updatedMonth' ,category = '$updatedCategory', amount = '$updatedAmount' WHERE id = '$id'";
            $db->query($updateSql);

            // Redirect back to the main page after saving changes
            header("Location: user.php?module=See%20All%20Claims&page=claims");
            exit();
        }
        ?>
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Edit Page</title>
        </head>
        <body>
            <h2>Edit Data</h2>
            <form method="post" class="edit_form">
                <label class = "edit_label" for="updated_date">Date:</label>
                <input class="edit_input" type="text" id="updated_date" name="updated_date" value="<?php echo $row['date']; ?>" required>

                <label class = "edit_label" for="updated_month">Month:</label>
                <input class="edit_input" type="text" id="updated_month" name="updated_month" value="<?php echo $row['month']; ?>" required>

                <label class = "edit_label" for="updated_category">Category:</label>
                <input class="edit_input" type="text" id="updated_category" name="updated_category" value="<?php echo $row['category']; ?>" required>

                <label class = "edit_label" for="updated_amount">Amount:</label>
                <input class="edit_input" type="text" id="updated_amount" name="updated_amount" value="<?php echo $row['amount']; ?>" required>

                <button class = "edit_button" type="submit" name="save">Save Changes</button>
            </form>
        </body>
        </html>
        <?php
    } else {
        // If no record found for the given ID
        echo "Record not found.";
    }
} else {
    // If ID parameter is not set
    echo "Invalid request. Please provide an ID.";
}
?>
