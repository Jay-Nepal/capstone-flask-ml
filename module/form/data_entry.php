<?php

$identry = isset($_GET['id']);

if(isset($_POST['post'])==1){
    $category = $_POST['slxCategory'];
    $description = $_POST['description'];
    $quantity = $_POST['quantity'];
    $price = $_POST['price'];
    $currDate = date("Y-m-d H:i:s");
    $identry = $_POST['identry'];

    if($identry > 0){
        $sql = "UPDATE data_entry SET category='$category', `description`='$description', quantity='$quantity', price='$price' WHERE = id='$identry'";
    } else {
        // insert into tbl_entry
        $sql = "INSERT INTO data_entry (category, `description`, quantity, price, created_date) VALUES ('$category', '$description','$quantity', '$price', '$currDate')";
    }

    $db->query($sql);
}

?>
<form action="" method="POST">
    <div class="row">
        <div class="col">
            <label for="">Select</label>
            <select name="slxCategory" class="form-control" id="">
                <option value="">- SELECT -</option>
                <option value="1">Category 1</option>
                <option value="2">Category 2</option>
            </select>
        </div>
        <div class="col">
            
        </div>
    </div>
    <div class="row">
        <div class="col">
            <label for="">Description</label>
            <textarea name="description" class="form-control" id="" cols="30" rows="10"></textarea>
        </div>
    </div>
    <div class="row mb-3">
        <div class="col">
            <label for="">Quantity</label>
            <input type="number" name="quantity" class="form-control" min="0">
        </div>
        <div class="col">
            <label for="">Price</label>
            <input type="text" class="form-control" name="price">
        </div>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
    <input type="hidden" name="post" value="1">
    <input type="hidden" name="identry" value="<?php $id_entry;?>">
</form>

<!-- <div class="mb-3">
        <label for="exampleInputEmail1" class="form-label">Email address</label>
        <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
        <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
    </div>
    <div class="mb-3">
        <label for="exampleInputPassword1" class="form-label">Password</label>
        <input type="password" class="form-control" id="exampleInputPassword1">
    </div>
    <div class="mb-3 form-check">
        <input type="checkbox" class="form-check-input" id="exampleCheck1">
        <label class="form-check-label" for="exampleCheck1">Check me out</label>
    </div> -->