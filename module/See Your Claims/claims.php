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
</style>

<?php

if (isset($_SESSION['email'])) {
    $email = $_SESSION['email'];
    $db = new myConnection();

    // Fetch data from the MySQL table
    $sql = "SELECT id, date, month, email, category, amount FROM chart_data where email = '$email'";
    $result = $db->query($sql);
}

if ($result->num_rows > 0) {
    // Display table header
    echo "<table><tr><th>Date</th><th>Category</th><th>Amount</th></tr>";

    // Output data of each row
    while ($row = $result->fetch_assoc()) {
        echo "<tr><td>" . $row["date"] . "</td><td>" . $row["category"] . "</td><td> RM " . $row["amount"] . "</td></tr>";
    }

    // Close table
    echo "</table>";
} else {
    echo "0 claims";
}

?>