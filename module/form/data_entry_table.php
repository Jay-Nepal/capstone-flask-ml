<?php


if(isset($_POST['post'])==1){
    //$file = $_FILES['image']['name'];
    $category = $_POST['category'];
    $currDate = date("Y-m-d H:i:s");
  

    foreach($category as $bil => $categ){
        $category = $categ;
        $price = $_POST['price'][$bil];
        $description = $_POST['description'][$bil];
        $quantity = $_POST['quantity'][$bil];
      

       
        
       
        
        $sql = "INSERT INTO data_entry2 (category, `description`, quantity, price, created_date) VALUES ('$category', '$description','$quantity', '$price', '$currDate')";

        $db->query($sql);

      

    }



    // $db->pageredirect();
     //die();

}


?>

<form action="" method="POST">
<table class="table table-striped">
    <thead>
        <tr>
            <th>Category</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Description</th>
         
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <select name="category[]" class="form-control" id="">
                    <option value="0">- SELECT -</option>
                    <option value="1">Category 1</option>
                    <option value="2">Category 2</option>
                </select>
            </td>
            <td>
                <input type="text" class="form-control" name="price[]">
            </td>
            <td>
                <input type="text" class="form-control" name="quantity[]">
            </td>
            <td>
                <input type="text" class="form-control" name="description[]">
            </td>
           
        </tr>
        <tr>
            <td>
                <select name="category[]" class="form-control" id="">
                    <option value="0">- SELECT -</option>
                    <option value="1">Category 1</option>
                    <option value="2">Category 2</option>
                </select>
            </td>
            <td>
                <input type="text" class="form-control" name="price[]">
            </td>
            <td>
                <input type="text" class="form-control" name="quantity[]">
            </td>
            <td>
                <input type="text" class="form-control" name="description[]">
            </td>
           
        </tr>
        <tr>
            <td>
                <select name="category[]" class="form-control" id="">
                    <option value="0">- SELECT -</option>
                    <option value="1">Category 1</option>
                    <option value="2">Category 2</option>
                </select>
            </td>
            <td>
                <input type="text" class="form-control" name="price[]">
            </td>
            <td>
                <input type="text" class="form-control" name="quantity[]">
            </td>
            <td>
                <input type="text" class="form-control" name="description[]">
            </td>
          
        </tr>
        <tr>
            <td>
                <select name="category[]" class="form-control" id="">
                    <option value="0">- SELECT -</option>
                    <option value="1">Category 1</option>
                    <option value="2">Category 2</option>
                </select>
            </td>
            <td>
                <input type="text" class="form-control" name="price[]">
            </td>
            <td>
                <input type="text" class="form-control" name="quantity[]">
            </td>
            <td>
                <input type="text" class="form-control" name="description[]">
            </td>
           
        </tr>
    </tbody>
</table>

<input type="hidden" name="post" value="1">
<button class="btn btn-primary">Submit</button>
</form>

<div class="mb-3 mt-3">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Category</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Description</th>
             
            </tr>
        </thead>
        <tbody>
        <?php
                $sql = "SELECT * FROM `data_entry2`";
                // echo $sql;
                $res = $db->query($sql);
                while($data = $res->fetch_array()){
                    $bil;
                    $category = $data['category'];
                    $price = $data['price'];
                    $quantity = $data['quantity'];
                    $description = $data['description'];
                  
                    

                    echo "<tr>";
                    echo "<td>Category $category</td>";
                    echo "<td>$price</td>";
                    echo "<td>$quantity</td>";
                    echo "<td>$description</td>";
                 
                    echo "</tr>";

                   
                }
            ?>
        </tbody>
    </table>
</div>