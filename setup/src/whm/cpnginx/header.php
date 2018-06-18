<?php
ob_start();
session_start();
extract($_POST);
extract($_GET);
$urlPath = $_SERVER['REQUEST_URI'];
$urlPathArray = basename($_SERVER['PHP_SELF']);
include 'lib/common.php';
$disable_Cpginx = '/etc/cpnginx/disablecpnginx';

if (file_exists($disable_Cpginx)) {
	header('Location: ./disable_cpnginx.php');
	exit();
}

$license = 'OK';

if ($license != 'OK') {
	header('Location: ./cpnginx.php');
	exit();
}

echo "\n" . '<!DOCTYPE html>' . "\n" . '<html>' . "\n" . '  <head>' . "\n" . '    <meta charset="utf-8">' . "\n" . '    <meta http-equiv="X-UA-Compatible" content="IE=edge">' . "\n" . '    <!-- responsive to screen width -->' . "\n" . '    <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">' . "\n" . '    <meta http-equiv="X-UA-Compatible" content="IE=9" />' . "\n" . '    <link rel="stylesheet" href="css/bootstrap.min.css">' . "\n" . '    <!-- Font Awesome -->' . "\n" . '    <link rel="stylesheet" href="css/font-awesome.min.css">' . "\n" . '    <link rel="stylesheet" href="css/ionicons.min.css">' . "\n" . '    <!-- Theme style -->' . "\n" . '    <link rel="stylesheet" href="css/AdminLTE.css">' . "\n" . '    <link rel="stylesheet" href="css/skin-green.css">' . "\n" . '    ' . "\n" . '    <!-- custom style -->' . "\n" . '    <link rel="stylesheet" href="css/style.css"> ' . "\n" . '    <script src="js/jquery-2.1.4.min.js" type="text/javascript"></script>' . "\n" . '    <!-- juery ui js (ex: popup window)-->' . "\n" . '    <script src="js/jquery-ui.min.js" type="text/javascript"></script>' . "\n" . '    ' . "\n" . '    ';
include 'get_language.php';
echo '    ';

?>
