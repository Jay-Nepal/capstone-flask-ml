<?php

include("../include/mysql.php");

$db = new myConnection;

$sql = "CREATE TABLE users (
    id int(11) NOT NULL AUTO_INCREMENT,
    name varchar(255) DEFAULT NULL,
    email varchar(255) DEFAULT NULL,
    password varchar(255) DEFAULT NULL,
    role int(11) DEFAULT NULL,
    UNIQUE KEY PRIMARY_KEY (id) USING BTREE
  ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;";

$res = $db->query($sql);
if($res){

    $insert = "INSERT INTO users (id, name, email, password, role) VALUES
    (1, 'demo', 'demo@testing.com', '$2y$10$X0KsIDYx3/TmUyVn8QNgauvprWup5iqWxWxv3jVt5Bju7KPJEtZrm', 1)";
    $db->query($insert);

}

  