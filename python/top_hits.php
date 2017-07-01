<?php

$inputFile = fopen("top_hits.txt", "r") or die("Unable to open file!");
$input_lines = fread($inputFile,filesize("top_hits.txt"));
preg_match_all("/<tr> <td>([^<DATE>]*)<\/td> <td>([^<>]*)<\/td> <td>([^<>]*)<\/td> <td>([^<>]*)<\/td> <\/tr>/", $input_lines, $output_array);

$outputFile = fopen("top_hits.csv", "w") or die("Unable to open file!");
for ($i=0; $i < count($output_array[1]); $i++) { 
   $line = $output_array[1][$i].",".$output_array[2][$i].",".$output_array[3][$i].",".$output_array[4][$i]."\n";
   $line = str_replace('&amp;', '&', $line);
   fwrite($outputFile, $line);
}

fclose($outputFile);
?>