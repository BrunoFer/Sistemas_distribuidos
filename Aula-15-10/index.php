<?php

$db = pg_connect("host=10.3.1.52 dbname=AulaSD user=postgres password=123456 port=5432");
if($db){
    $result = pg_query($db, "SELECT * FROM \"Alunos\";");
    echo "Alunos matriculados disciplina:<br /><br />";
    while($row = pg_fetch_array($result)){
	echo $row[0];
	echo "<br>";
    }
}
else{
    echo "b";
}

echo "<center><a href='aprovados.php'>Alunos Aprovados<a>   -   ";
echo "<a href='reprovados.php'>Alunos Reprovados</a></center>"

?>
