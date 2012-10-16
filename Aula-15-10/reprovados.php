<?php

$db = pg_connect("host=10.3.1.52 dbname=AulaSD user=postgres password=123456 port=5432");
if($db){
    $result = pg_query($db, "SELECT * FROM \"Alunos\" WHERE \"Nota\"<6;");
    echo "Alunos matriculados disciplina:<br /><br />";
    while($row = pg_fetch_array($result)){
	echo $row[0];
	echo "<br>";
    }
}
else{
    echo "b";
}

echo "<b><center><a href='index.php'>Inicio</a></center>";

?>
