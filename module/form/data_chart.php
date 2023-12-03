<?php

if(isset($_POST['post'])==1){
    // file yang di upload
    $file_csv = $_FILES['file']['tmp_name'];

    // check kalau file ni ada value 
    if($_FILES['file']['size'] > 0){

        // open file_csv
        $file = fopen($file_csv,"r");
        while(($data = fgetcsv($file, 1000, ",")) != FALSE){
            $date = $data[0];
            $month = $data[1];
            $dept = $data[2];
            $status_invoice = $data[3];
            $po_amount = $data[4];
            if($date <> "Date"){
                $sql = "INSERT INTO chart_data (date, month, dept, status_invoice, po_amount ) VALUES ('$date','$month','$dept','$status_invoice', '$po_amount') ";
                // echo $sql;
                $db->query($sql);
            }
        }
    }

    $db->pageredirect("mainpage.php?module=form&page=data_chart");
   
}


?>


<form action="" method="POST" enctype="multipart/form-data">
    <input type="file" name="file" class="form-control mb-3">
    <button class="btn btn-primary">Upload</button>
    <input type="hidden" name="post" value="1">
</form>

<div class="mb-3">
    <h2>Data For Chart</h2>
    <table class="table table-striped table-hover">
        <thead>
            <th>Dept</th>
            <th>PO Amount</th>
            
        </thead>
        <tbody>
            <?php

                $sqldata = "SELECT  dept, po_amount FROM chart_data";
                $querydata = $db->query($sqldata);
                while($getdata = $querydata->fetch_array()){
                   // $date = $getdata['date'];
                   // $month = $getdata['month'];
                    $dept = $getdata['dept'];
                    //$status_invoice = $getdata['status_invoice'];
                    $po_amount = $getdata['po_amount'];
                  
                    

                    echo "<tr>";
                   // echo "<td>$date</td>";
                    //echo "<td>$month</td>";
                    echo "<td>$dept</td>";
                    echo "<td>$po_amount</td>";
                
                    echo "</tr>";

                }

            ?>
        </tbody>
    </table>
</div>