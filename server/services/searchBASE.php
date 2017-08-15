<?php

header('Content-type: application/json');

require_once dirname(__FILE__) . '/../classes/headstart/library/CommUtils.php';
require_once dirname(__FILE__) . '/../classes/headstart/library/toolkit.php';
require_once dirname(__FILE__) . '/../classes/headstart/preprocessing/Snapshot.php';
require 'search.php';

use headstart\library;

$INI_DIR = dirname(__FILE__) . "/../preprocessing/conf/";
$ini_array = library\Toolkit::loadIni($INI_DIR);
$service = array("name" => "BASE", "service" => "base");

$dirty_query = library\CommUtils::getParameter($_POST, "q");

$post_params = $_POST;

$result = search("base", $dirty_query, $post_params, array("from", "to", "document_types"), ";", null);

echo $result

?>
