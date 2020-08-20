<?php

require_once dirname(__FILE__) . '../../headstart/preprocessing/spellchecking/QuerySpellchecking.php';
require_once dirname(__FILE__) . '../../headstart/library/toolkit.php';

use headstart\library;

$INI_DIR = dirname(__FILE__) . "../../../preprocessing/conf/";
$ini_array = library\Toolkit::loadIni($INI_DIR);

$spellchecking = new \headstart\preprocessing\spellchecking\QuerySpellchecking($ini_array);    

if (($output_handle = fopen("test_output.csv", "w+")) !== FALSE) {
    fputcsv($output_handle, array("query", "corrected_query", "expected_query", "query_match", "sc_array"
                                    , "detected_language", "expected_language", "language_match"
                                    , "ld_array"));
} else {
    die("Could not create output file");
}

if (($input_handle = fopen("test_queries.csv", "r")) !== FALSE) {
    while (($data = fgetcsv($input_handle, 1000, ",")) !== FALSE) {
        $expected_language = (isset($data[1])?($data[1]):(""));
        $expected_query = (isset($data[2])?($data[2]):(""));
        
        echo $data[0] . "\n";
        
        $results = $spellchecking->performSpellchecking($data[0], true);
        $corrected_query = $results["new_query"];
        $detected_language = array_keys($results["language_detection"]["ld_array"])[0];
        
        $language_match = ($expected_language !== "")?($expected_language === $detected_language):("");
        $query_match = ($expected_query !== "")?($expected_query === $corrected_query):("");
    
        fputcsv($output_handle, array(
                    $data[0]
                    , $corrected_query
                    , $expected_query
                    , $query_match ? 'true' : 'false'
                    , json_encode($results["spellcheck"])
                    , $detected_language
                    , $expected_language
                    , $language_match ? 'true' : 'false'
                    , json_encode($results["language_detection"]["ld_array"])
                ));
    }
    fclose($input_handle);
} else {
    die("Could not read input file");
}
