<?php

class myConnection
{
    // __construct run after call myConnection
    function __construct(){

        $host = "localhost";
        $user = "root";
        $pass = "";
        $db = "lightXpense";

        $conn = $this->mysqli = new mysqli($host,$user,$pass,$db);

        if ($conn->connect_errno) {
			printf("Connect failed: %s\n", $conn->connect_error);
			exit();
		}


    }  

    // nak pendekkan query writing
    function query($query){
		return $this->mysqli->query($query);
	}

    function num_rows($query){
        
        if($query)
            $rows = $this->mysqli->num_rows($query);
        else
            $rows=0;
       
        return $rows;
    }

    function pageredirect($url){
		echo "<script type='text/javascript'>location.href='$url'</script>";
	}

    function signout(){
        return $this->pageredirect("index.php");
    }
// data query by month
// where month is set by its relevant label
    function data_chart_by_month($email){
        $datamon = [];
        $month = [1,2,3,4,5,6,7,8,9,10,11,12];

        foreach($month as $mon){
            $data = 0;  // Reset $data for each month
            $sqldata = "SELECT date, month, category, amount FROM chart_data WHERE month='$mon' AND email='$email'";
            $querydata = $this->query($sqldata);
        
            while($getdata = $querydata->fetch_array()){
                $data += $getdata['amount'];
            }
        
            $datamon[$mon] = $data;
        }

        return $datamon;
    }

    function data_chart_by_month_admin(){
        $datamon = [];
        $month = [1,2,3,4,5,6,7,8,9,10,11,12];

        foreach($month as $mon){
            $data = 0;  // Reset $data for each month
            $sqldata = "SELECT date, month, category, amount FROM chart_data WHERE month='$mon'";
            $querydata = $this->query($sqldata);
        
            while($getdata = $querydata->fetch_array()){
                $data += $getdata['amount'];
            }
        
            $datamon[$mon] = $data;
        }

        return $datamon;
    }


    function category(){
        $array = [];
        $sqldata = "SELECT category FROM chart_data GROUP BY category";
        //echo $sqldata;
        $resdata = $this->query($sqldata);
        while($getdata = $resdata->fetch_array()){
            $array[] = $getdata['category'];
           //$data += $getdata['status_invoice'];
        }

        return $array;
    }

    function data_chart_by_category($email){
        $datamon = [];
        $category = $this->category();

        foreach ($category as $sta) {
            $data = 0;  // Reset $data for each category
            $sqldata = "SELECT amount FROM chart_data WHERE category='$sta' AND email = '$email'";
            $querydata = $this->query($sqldata);

            while ($getdata = $querydata->fetch_array()) {
                $data += $getdata['amount'];
            }

            $datamon[$sta] = $data;
        }

        return $datamon;
    }

    function data_chart_by_category_admin(){
        $datamon = [];
        $category = $this->category();

        foreach ($category as $sta) {
            $data = 0;  // Reset $data for each category
            $sqldata = "SELECT amount FROM chart_data WHERE category='$sta'";
            $querydata = $this->query($sqldata);

            while ($getdata = $querydata->fetch_array()) {
                $data += $getdata['amount'];
            }

            $datamon[$sta] = $data;
        }

        return $datamon;
    }

    function total_amount($email){
        $total = 0;
        $sqldata = "SELECT amount FROM chart_data where email = '$email'";
        $querydata = $this->query($sqldata);

        while($getdata = $querydata->fetch_array()){
            $total += $getdata['amount'];
        }

        return $total;
    }

    function total_amount_admin(){
        $total = 0;
        $sqldata = "SELECT amount FROM chart_data";
        $querydata = $this->query($sqldata);

        while($getdata = $querydata->fetch_array()){
            $total += $getdata['amount'];
        }

        return $total;
    }

    function number_claims($email){
        $totalClaims = 0;
        $sqldata = "SELECT COUNT(id) AS claim_count FROM chart_data where email = '$email'";
        $querydata = $this->query($sqldata);

        if ($querydata) {
            $result = $querydata->fetch_assoc();
            $totalClaims = $result['claim_count'];
        }

        return $totalClaims;
    }

    function number_claims_admin(){
        $totalClaims = 0;
        $sqldata = "SELECT COUNT(id) AS claim_count FROM chart_data";
        $querydata = $this->query($sqldata);

        if ($querydata) {
            $result = $querydata->fetch_assoc();
            $totalClaims = $result['claim_count'];
        }

        return $totalClaims;
    }

    function count_distinct_categories($email){
        $sqldata = "SELECT COUNT(DISTINCT category) AS category_count FROM chart_data WHERE email = '$email'";
        $querydata = $this->query($sqldata);

        $categoryCount = 0;

        if ($querydata) {
            $result = $querydata->fetch_assoc();
            $categoryCount = $result['category_count'];
        }

        return $categoryCount;
    }
    
    function count_distinct_categories_admin(){
        $sqldata = "SELECT COUNT(DISTINCT category) AS category_count FROM chart_data";
        $querydata = $this->query($sqldata);

        $categoryCount = 0;

        if ($querydata) {
            $result = $querydata->fetch_assoc();
            $categoryCount = $result['category_count'];
        }

        return $categoryCount;
    }
}