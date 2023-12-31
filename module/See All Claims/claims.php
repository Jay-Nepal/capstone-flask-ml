<style>
    table {
        border-collapse: collapse;
        width: 100%;
        margin-top: 20px;
    }

    table, th, td {
        border: 1px solid #ddd;
    }

    th, td {
        padding: 10px;
        /* text-align: left; */
    }

    th {
        background-color: #f2f2f2;
    }

    th.edit-column {
        width: 100px; /* Adjust the width as needed */
        text-align: center; /* Center the content within th elements */
    }

    /* Adjust the width of the Edit button column */
    td.edit-column {
        width: 100px; /* Adjust the width as needed */
        text-align: center; /* Center the content within th elements */
    }

    /* Style for the Edit button */
    button.edit-button {
        width: 100%;
        padding: 5px;
        box-sizing: border-box;
    }
</style>

<?php

if(isset($_SESSION['email'])) {
    $email = $_SESSION['email'];
    $db = new myConnection(); 

    // Fetch data from the MySQL table
    $sql = "SELECT id, user_details.first_name as firstName, date, month, category, amount FROM chart_data LEFT JOIN user_details on user_details.email = chart_data.email";
    $result = $db->query($sql);
}

if ($result->num_rows > 0) {
    // Display table header
    echo "<table><tr><th>Employee</th><th>Date</th><th>Category</th><th>Amount</th><th class='edit-column'>Edit</th></tr>";

    // Output data of each row
    while ($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["firstName"] . "</td><td>" . $row["date"] . "</td><td>" . $row["category"] . "</td><td> RM " . $row["amount"] . "</td>";
        
        echo "<td class='edit-column'><button class='edit-button' onclick=\"editRow(" . $row["id"] . ")\">Edit</button></td>
        </tr>";
    }

    // Close table
    echo "</table>";
} else {
    echo "0 results";
}

?>

<!-- Add JavaScript function for editing -->
<script>
    function editRow(id) {
        // Redirect to the edit page with the specific row ID
        window.location.href = "user.php?module=See%20All%20Claims&page=edit_page&id=" + id;
    }
</script>
