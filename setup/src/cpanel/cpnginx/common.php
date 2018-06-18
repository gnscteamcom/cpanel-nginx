<?php
class Builder
{
	public function header($filename, $data)
	{
		include $filename . '.php';
	}

	public function footer($filename)
	{
		include $filename . '.php';
	}

	public function view($filename, $data)
	{
		include $filename . '.php';
	}

	public function find_user_home($user)
	{
		$lines = file('/etc/passwd');

		foreach ($lines as $key) {
			$term = explode(':', trim($key));

			return $term[5];
		}
	}

	public function json_validate($string, $file)
	{
		$result = json_decode($string);

		switch (json_last_error()) {
		case JSON_ERROR_NONE:
			$error = '';
			break;

		case JSON_ERROR_DEPTH:
			$error = 'The maximum stack depth has been exceeded.';
			break;

		case JSON_ERROR_STATE_MISMATCH:
			$error = 'Invalid or malformed JSON.';
			break;

		case JSON_ERROR_CTRL_CHAR:
			$error = 'Control character error, possibly incorrectly encoded.';
			break;

		case JSON_ERROR_SYNTAX:
			$error = 'Syntax error, malformed JSON.';
			break;

		case JSON_ERROR_UTF8:
			$error = 'Malformed UTF-8 characters, possibly incorrectly encoded.';
			break;

		case JSON_ERROR_RECURSION:
			$error = 'One or more recursive references in the value to be encoded.';
			break;

		case JSON_ERROR_INF_OR_NAN:
			$error = 'One or more NAN or INF values in the value to be encoded.';
			break;

		case JSON_ERROR_UNSUPPORTED_TYPE:
			$error = 'A value of a type that cannot be encoded was given.';
			break;
		}

		if ($error !== '') {
			unset($file);
		}

		return $error;
	}

	public function get_userdomainjson($user_home, $domain)
	{
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		$localdata = array();

		if (file_exists($fileName)) {
			if (!is_link($fileName)) {
				$file = file_get_contents($fileName);
				$var = $this->json_validate($file, $fileName);

				if ($var == '') {
					$localdata = json_decode($file, true);
				}
				else {
					$localdata = array();
				}
			}
			else {
				$localdata = array();
			}
		}
		else {
			$localdata = array();
		}

		$settings = $this->get_settings();
		$firewall = $this->get_firewall();
		$finaldata = array();

		if (!empty($localdata)) {
			$fpm = file_get_contents('/etc/cpnginx/data/fpm.json');
			$fpm_Data = json_decode($fpm, true);
			$tempData = file_get_contents('/etc/cpnginx/data/templates.json');
			$temp_Data = json_decode($tempData, true);

			if (array_key_exists('PHP_FPM', $localdata)) {
				if (array_key_exists($localdata['PHP_FPM'][0], $fpm_Data)) {
					$finaldata['PHP_FPM'][0] = $localdata['PHP_FPM'][0];
				}
				else {
					$finaldata['PHP_FPM'][0] = $settings['PHP_FPM'][0];
				}
			}
			else {
				$finaldata['PHP_FPM'][0] = $settings['PHP_FPM'][0];
			}

			if (array_key_exists('WEB_SERVER', $localdata)) {
				if (array_key_exists($localdata['WEB_SERVER'][0], $temp_Data)) {
					$finaldata['WEB_SERVER'][0] = $localdata['WEB_SERVER'][0];
				}
				else {
					$finaldata['WEB_SERVER'][0] = $settings['WEB_SERVER'][0];
				}
			}
			else {
				$finaldata['WEB_SERVER'][0] = $settings['WEB_SERVER'][0];
			}

			if ($settings['DIRECTORY_LIST'][0] == '1') {
				if (array_key_exists('DIRECTORY_LIST', $localdata) && (($localdata['DIRECTORY_LIST'][0] == '1') || ($localdata['DIRECTORY_LIST'][0] == '0'))) {
					$finaldata['DIRECTORY_LIST'][0] = $localdata['DIRECTORY_LIST'][0];
				}
				else {
					$finaldata['DIRECTORY_LIST'][0] = $settings['DIRECTORY_LIST'][0];
				}
			}
			else {
				$finaldata['DIRECTORY_LIST'][0] = $settings['DIRECTORY_LIST'][0];
			}

			if ($settings['HOT_LINK_PROTECTION'][0] == '1') {
				if (array_key_exists('HOT_LINK_PROTECTION', $localdata) && (($localdata['HOT_LINK_PROTECTION'][0] == '1') || ($localdata['HOT_LINK_PROTECTION'][0] == '0'))) {
					$finaldata['HOT_LINK_PROTECTION'][0] = $localdata['HOT_LINK_PROTECTION'][0];
				}
				else {
					$finaldata['HOT_LINK_PROTECTION'][0] = $settings['HOT_LINK_PROTECTION'][0];
				}
			}
			else {
				$finaldata['HOT_LINK_PROTECTION'][0] = $settings['HOT_LINK_PROTECTION'][0];
			}

			if ($settings['MOD_FLV'][0] == '1') {
				if (array_key_exists('MOD_FLV', $localdata) && (($localdata['MOD_FLV'][0] == '1') || ($localdata['MOD_FLV'][0] == '0'))) {
					$finaldata['MOD_FLV'][0] = $localdata['MOD_FLV'][0];
				}
				else {
					$finaldata['MOD_FLV'][0] = $settings['MOD_FLV'][0];
				}
			}
			else {
				$finaldata['MOD_FLV'][0] = $settings['MOD_FLV'][0];
			}

			if ($settings['MOD_MP4'][0] == '1') {
				if (array_key_exists('MOD_MP4', $localdata) && (($localdata['MOD_MP4'][0] == '1') || ($localdata['MOD_MP4'][0] == '0'))) {
					$finaldata['MOD_MP4'][0] = $localdata['MOD_MP4'][0];
				}
				else {
					$finaldata['MOD_MP4'][0] = $settings['MOD_MP4'][0];
				}
			}
			else {
				$finaldata['MOD_MP4'][0] = $settings['MOD_MP4'][0];
			}

			if ($settings['GOOGLE_PAGE_SPEED'][0] == '1') {
				if (array_key_exists('GOOGLE_PAGE_SPEED', $localdata) && (($localdata['GOOGLE_PAGE_SPEED'][0] == '1') || ($localdata['GOOGLE_PAGE_SPEED'][0] == '0'))) {
					$finaldata['GOOGLE_PAGE_SPEED'][0] = $localdata['GOOGLE_PAGE_SPEED'][0];
				}
				else {
					$finaldata['GOOGLE_PAGE_SPEED'][0] = $settings['GOOGLE_PAGE_SPEED'][0];
				}
			}
			else {
				$finaldata['GOOGLE_PAGE_SPEED'][0] = $settings['GOOGLE_PAGE_SPEED'][0];
			}

			if ($settings['PROXY_CACHE'][0] == '1') {
				if (array_key_exists('PROXY_CACHE', $localdata) && (($localdata['PROXY_CACHE'][0] == '1') || ($localdata['PROXY_CACHE'][0] == '0'))) {
					$finaldata['PROXY_CACHE'][0] = $localdata['PROXY_CACHE'][0];
				}
				else {
					$finaldata['PROXY_CACHE'][0] = $settings['PROXY_CACHE'][0];
				}
			}
			else {
				$finaldata['PROXY_CACHE'][0] = $settings['PROXY_CACHE'][0];
			}

			if ($settings['FASTCGI_CACHE'][0] == '1') {
				if (array_key_exists('FASTCGI_CACHE', $localdata) && (($localdata['FASTCGI_CACHE'][0] == '1') || ($localdata['FASTCGI_CACHE'][0] == '0'))) {
					$finaldata['FASTCGI_CACHE'][0] = $localdata['FASTCGI_CACHE'][0];
				}
				else {
					$finaldata['FASTCGI_CACHE'][0] = $settings['FASTCGI_CACHE'][0];
				}
			}
			else {
				$finaldata['FASTCGI_CACHE'][0] = $settings['FASTCGI_CACHE'][0];
			}

			if (array_key_exists('HTTPS_REDIRECTION', $localdata) && (($localdata['HTTPS_REDIRECTION'][0] == '1') || ($localdata['HTTPS_REDIRECTION'][0] == '0'))) {
				$finaldata['HTTPS_REDIRECTION'][0] = $localdata['HTTPS_REDIRECTION'][0];
			}
			else {
				$finaldata['HTTPS_REDIRECTION'][0] = $settings['HTTPS_REDIRECTION'][0];
			}

			if (array_key_exists('WWW_REDIRECTION', $localdata) && (($localdata['WWW_REDIRECTION'][0] == 'none') || ($localdata['WWW_REDIRECTION'][0] == 'wwwtonon') || ($localdata['WWW_REDIRECTION'][0] == 'nontowww'))) {
				$finaldata['WWW_REDIRECTION'][0] = $localdata['WWW_REDIRECTION'][0];
			}
			else {
				$finaldata['WWW_REDIRECTION'][0] = $settings['WWW_REDIRECTION'][0];
			}

			if ($firewall['RANGE_PROTECTION'][0] == '1') {
				if (array_key_exists('RANGE_PROTECTION', $localdata) && (($localdata['RANGE_PROTECTION'][0] == '1') || ($localdata['RANGE_PROTECTION'][0] == '0'))) {
					$finaldata['RANGE_PROTECTION'][0] = $localdata['RANGE_PROTECTION'][0];
				}
				else {
					$finaldata['RANGE_PROTECTION'][0] = $firewall['RANGE_PROTECTION'][0];
				}
			}
			else {
				$finaldata['RANGE_PROTECTION'][0] = $firewall['RANGE_PROTECTION'][0];
			}

			if ($firewall['HTTP_METHOD_ENABLE'][0] == '1') {
				if (array_key_exists('HTTP_METHOD_ENABLE', $localdata) && (($localdata['HTTP_METHOD_ENABLE'][0] == '1') || ($localdata['HTTP_METHOD_ENABLE'][0] == '0'))) {
					$finaldata['HTTP_METHOD_ENABLE'][0] = $localdata['HTTP_METHOD_ENABLE'][0];
				}
				else {
					$finaldata['HTTP_METHOD_ENABLE'][0] = $firewall['HTTP_METHOD_ENABLE'][0];
				}
			}
			else {
				$finaldata['HTTP_METHOD_ENABLE'][0] = $firewall['HTTP_METHOD_ENABLE'][0];
			}

			if ($firewall['USER_AGENT_ATTACK_PROTECTION'][0] == '1') {
				if (array_key_exists('USER_AGENT_ATTACK_PROTECTION', $localdata) && (($localdata['USER_AGENT_ATTACK_PROTECTION'][0] == '1') || ($localdata['USER_AGENT_ATTACK_PROTECTION'][0] == '0'))) {
					$finaldata['USER_AGENT_ATTACK_PROTECTION'][0] = $localdata['USER_AGENT_ATTACK_PROTECTION'][0];
				}
				else {
					$finaldata['USER_AGENT_ATTACK_PROTECTION'][0] = $firewall['USER_AGENT_ATTACK_PROTECTION'][0];
				}
			}
			else {
				$finaldata['USER_AGENT_ATTACK_PROTECTION'][0] = $firewall['USER_AGENT_ATTACK_PROTECTION'][0];
			}

			if ($firewall['REFERRER_SPAM_PROTECHTION'][0] == '1') {
				if (array_key_exists('REFERRER_SPAM_PROTECHTION', $localdata) && (($localdata['REFERRER_SPAM_PROTECHTION'][0] == '1') || ($localdata['REFERRER_SPAM_PROTECHTION'][0] == '0'))) {
					$finaldata['REFERRER_SPAM_PROTECHTION'][0] = $localdata['REFERRER_SPAM_PROTECHTION'][0];
				}
				else {
					$finaldata['REFERRER_SPAM_PROTECHTION'][0] = $firewall['REFERRER_SPAM_PROTECHTION'][0];
				}
			}
			else {
				$finaldata['REFERRER_SPAM_PROTECHTION'][0] = $firewall['REFERRER_SPAM_PROTECHTION'][0];
			}

			if ($firewall['SCANNER_ATTACK_PROTECTION'][0] == '1') {
				if (array_key_exists('SCANNER_ATTACK_PROTECTION', $localdata) && (($localdata['SCANNER_ATTACK_PROTECTION'][0] == '1') || ($localdata['SCANNER_ATTACK_PROTECTION'][0] == '0'))) {
					$finaldata['SCANNER_ATTACK_PROTECTION'][0] = $localdata['SCANNER_ATTACK_PROTECTION'][0];
				}
				else {
					$finaldata['SCANNER_ATTACK_PROTECTION'][0] = $firewall['SCANNER_ATTACK_PROTECTION'][0];
				}
			}
			else {
				$finaldata['SCANNER_ATTACK_PROTECTION'][0] = $firewall['SCANNER_ATTACK_PROTECTION'][0];
			}

			if ($firewall['XSS_PROTECTION'][0] == '1') {
				if (array_key_exists('XSS_PROTECTION', $localdata) && (($localdata['XSS_PROTECTION'][0] == '1') || ($localdata['XSS_PROTECTION'][0] == '0'))) {
					$finaldata['XSS_PROTECTION'][0] = $localdata['XSS_PROTECTION'][0];
				}
				else {
					$finaldata['XSS_PROTECTION'][0] = $firewall['XSS_PROTECTION'][0];
				}
			}
			else {
				$finaldata['XSS_PROTECTION'][0] = $firewall['XSS_PROTECTION'][0];
			}

			if ($firewall['XFRAME_ATTACK_PROTECTION'][0] == '1') {
				if (array_key_exists('XFRAME_ATTACK_PROTECTION', $localdata) && (($localdata['XFRAME_ATTACK_PROTECTION'][0] == '1') || ($localdata['XFRAME_ATTACK_PROTECTION'][0] == '0'))) {
					$finaldata['XFRAME_ATTACK_PROTECTION'][0] = $localdata['XFRAME_ATTACK_PROTECTION'][0];
				}
				else {
					$finaldata['XFRAME_ATTACK_PROTECTION'][0] = $firewall['XFRAME_ATTACK_PROTECTION'][0];
				}
			}
			else {
				$finaldata['XFRAME_ATTACK_PROTECTION'][0] = $firewall['XFRAME_ATTACK_PROTECTION'][0];
			}

			if ($firewall['PROTECT_SQL_INJECTION'][0] == '1') {
				if (array_key_exists('PROTECT_SQL_INJECTION', $localdata) && (($localdata['PROTECT_SQL_INJECTION'][0] == '1') || ($localdata['PROTECT_SQL_INJECTION'][0] == '0'))) {
					$finaldata['PROTECT_SQL_INJECTION'][0] = $localdata['PROTECT_SQL_INJECTION'][0];
				}
				else {
					$finaldata['PROTECT_SQL_INJECTION'][0] = $firewall['PROTECT_SQL_INJECTION'][0];
				}
			}
			else {
				$finaldata['PROTECT_SQL_INJECTION'][0] = $firewall['PROTECT_SQL_INJECTION'][0];
			}

			if ($firewall['PROTECT_FILE_INJECT'][0] == '1') {
				if (array_key_exists('PROTECT_FILE_INJECT', $localdata) && (($localdata['PROTECT_FILE_INJECT'][0] == '1') || ($localdata['PROTECT_FILE_INJECT'][0] == '0'))) {
					$finaldata['PROTECT_FILE_INJECT'][0] = $localdata['PROTECT_FILE_INJECT'][0];
				}
				else {
					$finaldata['PROTECT_FILE_INJECT'][0] = $firewall['PROTECT_FILE_INJECT'][0];
				}
			}
			else {
				$finaldata['PROTECT_FILE_INJECT'][0] = $firewall['PROTECT_FILE_INJECT'][0];
			}

			if ($firewall['PROTECT_COMMON_EXPLOITS'][0] == '1') {
				if (array_key_exists('PROTECT_COMMON_EXPLOITS', $localdata) && (($localdata['PROTECT_COMMON_EXPLOITS'][0] == '1') || ($localdata['PROTECT_COMMON_EXPLOITS'][0] == '0'))) {
					$finaldata['PROTECT_COMMON_EXPLOITS'][0] = $localdata['PROTECT_COMMON_EXPLOITS'][0];
				}
				else {
					$finaldata['PROTECT_COMMON_EXPLOITS'][0] = $firewall['PROTECT_COMMON_EXPLOITS'][0];
				}
			}
			else {
				$finaldata['PROTECT_COMMON_EXPLOITS'][0] = $firewall['PROTECT_COMMON_EXPLOITS'][0];
			}

			if ($firewall['SYMLINK_ATTACK'][0] == 'on') {
				if (array_key_exists('SYMLINK_ATTACK', $localdata) && (($localdata['SYMLINK_ATTACK'][0] == 'on') || ($localdata['SYMLINK_ATTACK'][0] == 'off'))) {
					$finaldata['SYMLINK_ATTACK'][0] = $localdata['SYMLINK_ATTACK'][0];
				}
				else {
					$finaldata['SYMLINK_ATTACK'][0] = $firewall['SYMLINK_ATTACK'][0];
				}
			}
			else {
				$finaldata['SYMLINK_ATTACK'][0] = $firewall['SYMLINK_ATTACK'][0];
			}
		}
		else {
			$finaldata['PHP_FPM'][0] = $settings['PHP_FPM'][0];
			$finaldata['WEB_SERVER'][0] = $settings['WEB_SERVER'][0];
			$finaldata['DIRECTORY_LIST'][0] = $settings['DIRECTORY_LIST'][0];
			$finaldata['HOT_LINK_PROTECTION'][0] = $settings['HOT_LINK_PROTECTION'][0];
			$finaldata['MOD_FLV'][0] = $settings['MOD_FLV'][0];
			$finaldata['MOD_MP4'][0] = $settings['MOD_MP4'][0];
			$finaldata['GOOGLE_PAGE_SPEED'][0] = $settings['GOOGLE_PAGE_SPEED'][0];
			$finaldata['PROXY_CACHE'][0] = $settings['PROXY_CACHE'][0];
			$finaldata['FASTCGI_CACHE'][0] = $settings['FASTCGI_CACHE'][0];
			$finaldata['HTTPS_REDIRECTION'][0] = $settings['HTTPS_REDIRECTION'][0];
			$finaldata['WWW_REDIRECTION'][0] = $settings['WWW_REDIRECTION'][0];
			$finaldata['RANGE_PROTECTION'][0] = $firewall['RANGE_PROTECTION'][0];
			$finaldata['HTTP_METHOD_ENABLE'][0] = $firewall['HTTP_METHOD_ENABLE'][0];
			$finaldata['USER_AGENT_ATTACK_PROTECTION'][0] = $firewall['USER_AGENT_ATTACK_PROTECTION'][0];
			$finaldata['REFERRER_SPAM_PROTECHTION'][0] = $firewall['REFERRER_SPAM_PROTECHTION'][0];
			$finaldata['SCANNER_ATTACK_PROTECTION'][0] = $firewall['SCANNER_ATTACK_PROTECTION'][0];
			$finaldata['XSS_PROTECTION'][0] = $firewall['XSS_PROTECTION'][0];
			$finaldata['XFRAME_ATTACK_PROTECTION'][0] = $firewall['XFRAME_ATTACK_PROTECTION'][0];
			$finaldata['PROTECT_SQL_INJECTION'][0] = $firewall['PROTECT_SQL_INJECTION'][0];
			$finaldata['PROTECT_FILE_INJECT'][0] = $firewall['PROTECT_FILE_INJECT'][0];
			$finaldata['PROTECT_COMMON_EXPLOITS'][0] = $firewall['PROTECT_COMMON_EXPLOITS'][0];
			$finaldata['SYMLINK_ATTACK'][0] = $firewall['SYMLINK_ATTACK'][0];
		}

		return $finaldata;
	}

	public function get_settings()
	{
		$file = file_get_contents('/etc/cpnginx/data/settings.json');
		$file_arr = json_decode($file, true);
		return $file_arr;
	}

	public function get_firewall()
	{
		$file = file_get_contents('/etc/cpnginx/data/firewall.json');
		$file_arr = json_decode($file, true);
		return $file_arr;
	}

	public function userdomain_update($user_home, $domain)
	{
		$settings = $this->get_settings();
		$firewall = $this->get_firewall();
		$fpm = file_get_contents('/etc/cpnginx/data/fpm.json');
		$fpm_Data = json_decode($fpm, true);
		$tempData = file_get_contents('/etc/cpnginx/data/templates.json');
		$temp_Data = json_decode($tempData, true);
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);

		if (array_key_exists($_POST['web_server'], $temp_Data)) {
			$file_arr['WEB_SERVER'][0] = $_POST['web_server'];
		}

		if (array_key_exists($_POST['php_version'], $fpm_Data)) {
			$file_arr['PHP_FPM'][0] = $_POST['php_version'];
		}

		if ($settings['DIRECTORY_LIST'][0] == '1') {
			if (($_POST['directory_listing'] == '1') || ($_POST['directory_listing'] == '0')) {
				$file_arr['DIRECTORY_LIST'][0] = $_POST['directory_listing'];
			}
		}

		if ($settings['HOT_LINK_PROTECTION'][0] == '1') {
			if (($_POST['hot_link'] == '1') || ($_POST['hot_link'] == '0')) {
				$file_arr['HOT_LINK_PROTECTION'][0] = $_POST['hot_link'];
			}
		}

		if ($settings['MOD_FLV'][0] == '1') {
			if (($_POST['pseudo_flv'] == '1') || ($_POST['pseudo_flv'] == '0')) {
				$file_arr['MOD_FLV'][0] = $_POST['pseudo_flv'];
			}
		}

		if ($settings['MOD_MP4'][0] == '1') {
			if (($_POST['pseudo_mp4'] == '1') || ($_POST['pseudo_mp4'] == '0')) {
				$file_arr['MOD_MP4'][0] = $_POST['pseudo_mp4'];
			}
		}

		if ($settings['GOOGLE_PAGE_SPEED'][0] == '1') {
			if (($_POST['google_pagespeed'] == '1') || ($_POST['google_pagespeed'] == '0')) {
				$file_arr['GOOGLE_PAGE_SPEED'][0] = $_POST['google_pagespeed'];
			}
		}

		if ($settings['PROXY_CACHE'][0] == '1') {
			if (($_POST['proxy_cache'] == '1') || ($_POST['proxy_cache'] == '0')) {
				$file_arr['PROXY_CACHE'][0] = $_POST['proxy_cache'];
			}
		}

		if ($settings['FASTCGI_CACHE'][0] == '1') {
			if (($_POST['fcgi_cache'] == '1') || ($_POST['fcgi_cache'] == '0')) {
				$file_arr['FASTCGI_CACHE'][0] = $_POST['fcgi_cache'];
			}
		}

		if (($_POST['domain_redirect'] == '1') || ($_POST['domain_redirect'] == '0')) {
			$file_arr['HTTPS_REDIRECTION'][0] = $_POST['domain_redirect'];
		}

		if (($_POST['redirection'] == 'none') || ($_POST['redirection'] == 'wwwtonon') || ($_POST['redirection'] == 'nontowww')) {
			$file_arr['WWW_REDIRECTION'][0] = $_POST['redirection'];
		}

		if ($firewall['RANGE_PROTECTION'][0] == '1') {
			if (($_POST['range_protection'] == '1') || ($_POST['range_protection'] == '0')) {
				$file_arr['RANGE_PROTECTION'][0] = $_POST['range_protection'];
			}
		}

		if ($firewall['HTTP_METHOD_ENABLE'][0] == '1') {
			if (($_POST['http_method'] == '1') || ($_POST['http_method'] == '0')) {
				$file_arr['HTTP_METHOD_ENABLE'][0] = $_POST['http_method'];
			}
		}

		if ($firewall['USER_AGENT_ATTACK_PROTECTION'][0] == '1') {
			if (($_POST['attacks'] == '1') || ($_POST['attacks'] == '0')) {
				$file_arr['USER_AGENT_ATTACK_PROTECTION'][0] = $_POST['attacks'];
			}
		}

		if ($firewall['REFERRER_SPAM_PROTECHTION'][0] == '1') {
			if (($_POST['refer_spam'] == '1') || ($_POST['refer_spam'] == '0')) {
				$file_arr['REFERRER_SPAM_PROTECHTION'][0] = $_POST['refer_spam'];
			}
		}

		if ($firewall['SCANNER_ATTACK_PROTECTION'][0] == '1') {
			if (($_POST['website_scanner_attack'] == '1') || ($_POST['website_scanner_attack'] == '0')) {
				$file_arr['SCANNER_ATTACK_PROTECTION'][0] = $_POST['website_scanner_attack'];
			}
		}

		if ($firewall['XSS_PROTECTION'][0] == '1') {
			if (($_POST['xxss_protection'] == '1') || ($_POST['xxss_protection'] == '0')) {
				$file_arr['XSS_PROTECTION'][0] = $_POST['xxss_protection'];
			}
		}

		if ($firewall['XFRAME_ATTACK_PROTECTION'][0] == '1') {
			if (($_POST['xframe_protection'] == '1') || ($_POST['xframe_protection'] == '0')) {
				$file_arr['XFRAME_ATTACK_PROTECTION'][0] = $_POST['xframe_protection'];
			}
		}

		if ($firewall['PROTECT_SQL_INJECTION'][0] == '1') {
			if (($_POST['sql_injection'] == '1') || ($_POST['sql_injection'] == '0')) {
				$file_arr['PROTECT_SQL_INJECTION'][0] = $_POST['sql_injection'];
			}
		}

		if ($firewall['PROTECT_FILE_INJECT'][0] == '1') {
			if (($_POST['file_injection'] == '1') || ($_POST['file_injection'] == '0')) {
				$file_arr['PROTECT_FILE_INJECT'][0] = $_POST['file_injection'];
			}
		}

		if ($firewall['PROTECT_COMMON_EXPLOITS'][0] == '1') {
			if (($_POST['protection_common'] == '1') || ($_POST['protection_common'] == '0')) {
				$file_arr['PROTECT_COMMON_EXPLOITS'][0] = $_POST['protection_common'];
			}
		}

		if ($firewall['SYMLINK_ATTACK'][0] == 'on') {
			if (($_POST['symlink_attack'] == 'on') || ($_POST['symlink_attack'] == 'off')) {
				$file_arr['SYMLINK_ATTACK'][0] = $_POST['symlink_attack'];
			}
		}

		$file = json_encode($file_arr, true);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		$directory_path = $user_home . '/.cpnginx';

		if (!is_dir($directory_path)) {
			mkdir($directory_path, 448);
		}

		if (file_exists($fileName)) {
			if (is_link($fileName)) {
				unlink($fileName);
			}
		}

		file_put_contents($fileName, $file);
	}

	public function userdomainfirewall_update($user_home, $domain)
	{
		$firewall = $this->get_firewall();
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);

		if ($firewall['RANGE_PROTECTION'][0] == '1') {
			if (($_POST['range_protection'] == '1') || ($_POST['range_protection'] == '0')) {
				$file_arr['RANGE_PROTECTION'][0] = $_POST['range_protection'];
			}
		}

		if ($firewall['HTTP_METHOD_ENABLE'][0] == '1') {
			if (($_POST['http_method'] == '1') || ($_POST['http_method'] == '0')) {
				$file_arr['HTTP_METHOD_ENABLE'][0] = $_POST['http_method'];
			}
		}

		if ($firewall['USER_AGENT_ATTACK_PROTECTION'][0] == '1') {
			if (($_POST['attacks'] == '1') || ($_POST['attacks'] == '0')) {
				$file_arr['USER_AGENT_ATTACK_PROTECTION'][0] = $_POST['attacks'];
			}
		}

		if ($firewall['REFERRER_SPAM_PROTECHTION'][0] == '1') {
			if (($_POST['refer_spam'] == '1') || ($_POST['refer_spam'] == '0')) {
				$file_arr['REFERRER_SPAM_PROTECHTION'][0] = $_POST['refer_spam'];
			}
		}

		if ($firewall['SCANNER_ATTACK_PROTECTION'][0] == '1') {
			if (($_POST['website_scanner_attack'] == '1') || ($_POST['website_scanner_attack'] == '0')) {
				$file_arr['SCANNER_ATTACK_PROTECTION'][0] = $_POST['website_scanner_attack'];
			}
		}

		if ($firewall['XSS_PROTECTION'][0] == '1') {
			if (($_POST['xxss_protection'] == '1') || ($_POST['xxss_protection'] == '0')) {
				$file_arr['XSS_PROTECTION'][0] = $_POST['xxss_protection'];
			}
		}

		if ($firewall['XFRAME_ATTACK_PROTECTION'][0] == '1') {
			if (($_POST['xframe_protection'] == '1') || ($_POST['xframe_protection'] == '0')) {
				$file_arr['XFRAME_ATTACK_PROTECTION'][0] = $_POST['xframe_protection'];
			}
		}

		if ($firewall['PROTECT_SQL_INJECTION'][0] == '1') {
			if (($_POST['sql_injection'] == '1') || ($_POST['sql_injection'] == '0')) {
				$file_arr['PROTECT_SQL_INJECTION'][0] = $_POST['sql_injection'];
			}
		}

		if ($firewall['PROTECT_FILE_INJECT'][0] == '1') {
			if (($_POST['file_injection'] == '1') || ($_POST['file_injection'] == '0')) {
				$file_arr['PROTECT_FILE_INJECT'][0] = $_POST['file_injection'];
			}
		}

		if ($firewall['PROTECT_COMMON_EXPLOITS'][0] == '1') {
			if (($_POST['protection_common'] == '1') || ($_POST['protection_common'] == '0')) {
				$file_arr['PROTECT_COMMON_EXPLOITS'][0] = $_POST['protection_common'];
			}
		}

		if ($firewall['SYMLINK_ATTACK'][0] == 'on') {
			if (($_POST['symlink_attack'] == 'on') || ($_POST['symlink_attack'] == 'off')) {
				$file_arr['SYMLINK_ATTACK'][0] = $_POST['symlink_attack'];
			}
		}

		$file = json_encode($file_arr, true);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		$directory_path = $user_home . '/.cpnginx';

		if (!is_dir($directory_path)) {
			mkdir($directory_path, 448);
		}

		if (file_exists($fileName)) {
			if (is_link($fileName)) {
				unlink($fileName);
			}
		}

		file_put_contents($fileName, $file);
	}

	public function userdomaincache_update($user_home, $domain)
	{
		$settings = $this->get_settings();
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);

		if ($settings['PROXY_CACHE'][0] == '1') {
			if (($_POST['proxy_cache'] == '1') || ($_POST['proxy_cache'] == '0')) {
				$file_arr['PROXY_CACHE'][0] = $_POST['proxy_cache'];
			}
		}

		if ($settings['FASTCGI_CACHE'][0] == '1') {
			if (($_POST['fcgi_cache'] == '1') || ($_POST['fcgi_cache'] == '0')) {
				$file_arr['FASTCGI_CACHE'][0] = $_POST['fcgi_cache'];
			}
		}

		if ($settings['GOOGLE_PAGE_SPEED'][0] == '1') {
			if (($_POST['google_pagespeed'] == '1') || ($_POST['google_pagespeed'] == '0')) {
				$file_arr['GOOGLE_PAGE_SPEED'][0] = $_POST['google_pagespeed'];
			}
		}

		$file = json_encode($file_arr, true);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		$directory_path = $user_home . '/.cpnginx';

		if (!is_dir($directory_path)) {
			mkdir($directory_path, 448);
		}

		if (file_exists($fileName)) {
			if (is_link($fileName)) {
				unlink($fileName);
			}
		}

		file_put_contents($fileName, $file);
	}

	public function userdomainredirections_update($user_home, $domain)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		if (($_POST['domain_redirect'] == '1') || ($_POST['domain_redirect'] == '0')) {
			$file_arr['HTTPS_REDIRECTION'][0] = $_POST['domain_redirect'];
		}

		$file = json_encode($file_arr, true);
		$directory_path = $user_home . '/.cpnginx';

		if (!is_dir($directory_path)) {
			mkdir($directory_path, 448);
		}

		if (file_exists($fileName)) {
			if (is_link($fileName)) {
				unlink($fileName);
			}
		}

		file_put_contents($fileName, $file);
	}

	public function userdomainwwwredirections_update($user_home, $domain)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		if (($_POST['redirection'] == 'none') || ($_POST['redirection'] == 'wwwtonon') || ($_POST['redirection'] == 'nontowww')) {
			$file_arr['WWW_REDIRECTION'][0] = $_POST['redirection'];
		}

		$file = json_encode($file_arr, true);
		$directory_path = $user_home . '/.cpnginx';

		if (!is_dir($directory_path)) {
			mkdir($directory_path, 448);
		}

		if (file_exists($fileName)) {
			if (is_link($fileName)) {
				unlink($fileName);
			}
		}

		file_put_contents($fileName, $file);
	}

	public function userdomaindirectory_update($user_home, $domain, $edit)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';

		if ($edit == 0) {
			$file_arr['DIRECTORY_LIST'][0] = 1;
		}

		if ($edit == 1) {
			$file_arr['DIRECTORY_LIST'][0] = 0;
		}

		$file = json_encode($file_arr, true);
		$settings = $this->get_settings();

		if ($settings['DIRECTORY_LIST'][0] == '1') {
			if (($edit == 0) || ($edit == 1)) {
				$directory_path = $user_home . '/.cpnginx';

				if (!is_dir($directory_path)) {
					mkdir($directory_path, 448);
				}

				if (file_exists($fileName)) {
					if (is_link($fileName)) {
						unlink($fileName);
					}
				}

				file_put_contents($fileName, $file);
			}
		}
	}

	public function userdomainhotlink_update($user_home, $domain, $edit)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';

		if ($edit == 0) {
			$file_arr['HOT_LINK_PROTECTION'][0] = 1;
		}

		if ($edit == 1) {
			$file_arr['HOT_LINK_PROTECTION'][0] = 0;
		}

		$file = json_encode($file_arr, true);
		$settings = $this->get_settings();

		if ($settings['HOT_LINK_PROTECTION'][0] == '1') {
			if (($edit == 0) || ($edit == 1)) {
				$directory_path = $user_home . '/.cpnginx';

				if (!is_dir($directory_path)) {
					mkdir($directory_path, 448);
				}

				if (file_exists($fileName)) {
					if (is_link($fileName)) {
						unlink($fileName);
					}
				}

				file_put_contents($fileName, $file);
			}
		}
	}

	public function usernginxsite_update($user_home, $domain, $edit)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';

		if ($edit == 1) {
			$file_arr['WEB_SERVER'][0] = 'proxy';
		}

		if ($edit == 2) {
			$file_arr['WEB_SERVER'][0] = 'hybrid';
		}

		if ($edit == 3) {
			$file_arr['WEB_SERVER'][0] = 'nginx';
		}

		$file = json_encode($file_arr, true);
		if (($edit == 1) || ($edit == 2) || ($edit == 3)) {
			$directory_path = $user_home . '/.cpnginx';

			if (!is_dir($directory_path)) {
				mkdir($directory_path, 448);
			}

			if (file_exists($fileName)) {
				if (is_link($fileName)) {
					unlink($fileName);
				}
			}

			file_put_contents($fileName, $file);
		}
	}

	public function userdomainwebserver_update($user_home, $domain)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		$file = json_encode($file_arr, true);
		$tempData = file_get_contents('/etc/cpnginx/data/templates.json');
		$temp_Data = json_decode($tempData, true);
		$file_arr['WEB_SERVER'][0] = $_POST['web_server'];
		$file = json_encode($file_arr, true);

		if (array_key_exists($_POST['web_server'], $temp_Data)) {
			$directory_path = $user_home . '/.cpnginx';

			if (!is_dir($directory_path)) {
				mkdir($directory_path, 448);
			}

			if (file_exists($fileName)) {
				if (is_link($fileName)) {
					unlink($fileName);
				}
			}

			file_put_contents($fileName, $file);
		}
	}

	public function userdomainphpversion_update($user_home, $domain)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		$file = json_encode($file_arr, true);
		$fpm = file_get_contents('/etc/cpnginx/data/fpm.json');
		$fpm_Data = json_decode($fpm, true);
		$file_arr['PHP_FPM'][0] = $_POST['php_version'];
		$file = json_encode($file_arr, true);

		if (array_key_exists($_POST['php_version'], $fpm_Data)) {
			$directory_path = $user_home . '/.cpnginx';

			if (!is_dir($directory_path)) {
				mkdir($directory_path, 448);
			}

			if (file_exists($fileName)) {
				if (is_link($fileName)) {
					unlink($fileName);
				}
			}

			file_put_contents($fileName, $file);
		}
	}

	public function userdomainapp_update($user_home, $domain)
	{
		$file_arr = array();
		$file_arr = $this->get_userdomainjson($user_home, $domain);
		$fileName = $user_home . '/.cpnginx/' . $domain . '.json';
		$file = json_encode($file_arr, true);
		$tempData = file_get_contents('/etc/cpnginx/data/templates.json');
		$temp_Data = json_decode($tempData, true);
		$file_arr['WEB_SERVER'][0] = $_POST['web_server'];
		$file = json_encode($file_arr, true);

		if (array_key_exists($_POST['web_server'], $temp_Data)) {
			$directory_path = $user_home . '/.cpnginx';

			if (!is_dir($directory_path)) {
				mkdir($directory_path, 448);
			}

			if (file_exists($fileName)) {
				if (is_link($fileName)) {
					unlink($fileName);
				}
			}

			file_put_contents($fileName, $file);
		}
	}

	public function get_domaininfo($res_arr)
	{
		$domainarr = array();

		foreach ($res_arr as $key => $val) {
			if ($key == 'parked_domains') {
				foreach ($val as $parkedomain) {
					$arr['domain'] = $parkedomain;
					$arr['domain_type'] = 'parked_domain';
					$arr['documentroot'] = $res_arr['main_domain']['documentroot'];
					$arr['ip'] = $res_arr['main_domain']['ip'];
					$arr['user'] = $res_arr['main_domain']['user'];
					$domainarr[$parkedomain] = $arr;
				}
			}
			else if ($key == 'main_domain') {
				$arr['domain'] = $val['domain'];
				$arr['domain_type'] = 'main_domain';
				$arr['documentroot'] = $val['documentroot'];
				$arr['ip'] = $val['ip'];
				$arr['user'] = $val['user'];
				$domainarr[$val['domain']] = $arr;
			}
			else {
				foreach ($val as $domains) {
					if ($domains['type'] == 'sub_domain') {
						$domain_type = 'sub_domain';
					}
					else {
						$domain_type = 'addon_domain';
					}

					$arr['domain'] = $domains['domain'];
					$arr['domain_type'] = $domain_type;
					$arr['documentroot'] = $domains['documentroot'];
					$arr['ip'] = $domains['ip'];
					$arr['user'] = $res_arr['main_domain']['user'];
					$domainarr[$domains['domain']] = $arr;
				}
			}
		}

		return $domainarr;
	}
}

$disable_Cpginx = '/etc/cpnginx/disablecpnginx';

if (file_exists($disable_Cpginx)) {
	include 'disable_cpnginx.php';
	exit();
}

include '/usr/local/cpanel/php/cpanel.php';
$cpanel = new CPANEL();
$get_attributes = $cpanel->uapi('Locale', 'get_attributes');
$lang_val = $get_attributes['cpanelresult']['result']['data'];

if (file_exists('languages/' . $lang_val['locale'] . '.php')) {
	$language = $lang_val['locale'];
}
else {
	$language = 'en';
}

include 'languages/' . $language . '.php';

?>
