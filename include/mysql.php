<?php

session_start();

class myConnection
{
    // __construct run after call myConnection
    function __construct(){

        $host = "sql113.byethost3.com";
        $user = "b3_35433977";
        $pass = "c0n3q18k";
        $db = "b3_35433977_lightxpense";

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
        session_destroy();
        return $this->pageredirect("index.php");
    }
// data query by month
// where month is set by its relevant label
    function data_chart_by_month(){
        $data = 0;
        $datamon = [];
        $month = [1,2,3,4,5,6,7,8,9,10,11,12];
        foreach($month as $mon){
            $sqldata = "SELECT date, month, dept, status_invoice, po_amount FROM chart_data WHERE month='$mon'";
            $querydata = $this->query($sqldata);
            //echo $sqldata;
            while($getdata = $querydata->fetch_array()){
                $data += $getdata['po_amount'];
            }
            $datamon[$mon] = $data;
        }
        

        return $datamon;
    }

    function invoice_status(){
        $array = [];
        $sqldata = "SELECT status_invoice FROM chart_data GROUP BY status_invoice";
        //echo $sqldata;
        $resdata = $this->query($sqldata);
        while($getdata = $resdata->fetch_array()){
            $array[] = $getdata['status_invoice'];
           //$data += $getdata['status_invoice'];
        }

        return $array;
    }

    function data_chart_by_status(){
        $data = 0;
        $datamon = [];
        $status = $this->invoice_status();

        foreach($status as $sta){
            $sqldata = "SELECT date, month, dept, status_invoice, po_amount FROM chart_data 
            WHERE status_invoice='$sta'";
            $querydata = $this->query($sqldata);
            while($getdata = $querydata->fetch_array()){
                $data += $getdata['po_amount'];
            }
            $datamon[$sta] = $data;

            echo $sqldata;
        }

        return $datamon;

    }

}
