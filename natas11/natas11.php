<?php
// Enter your code here, enjoy!
//source code begining
function xor_encrypt($in, $key_to_find) {
    $key = $key_to_find;
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}
//end source code

$cookie = 'HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg%3D';

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

$letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVNBM";

$first_candidates = [];

for ($i=0 ; $i< strlen($letters); $i++){
	$data =  base64_encode(xor_encrypt(json_encode($defaultdata),$letters[$i]));
	if ($cookie[0] == $data[0] ){
		echo $data;
		echo " ";
		echo $letters[$i];
		$first_candidates[] = $letters[$i];
		echo "\n";
	}
}

$temp = [];
$contador = 2;
$found_key = false;
while($contador < 10) {
	for($k=0; $k < count($first_candidates); $k++){
		if($contador<5){
			for ($i=0 ; $i< strlen($letters); $i++){
				$key = $first_candidates[$k].$letters[$i];
				$data =  base64_encode(xor_encrypt(json_encode($defaultdata),$key));
				if (substr($cookie,0,$contador)==substr($data,0,$contador) ){
					echo $data;
					echo " ";
					echo $key;
					$temp[] = $key;
					echo "\n";
				}
			}
		}
		else{
			$found_key = true;
			$key = $first_candidates[$k];
			$data =  base64_encode(xor_encrypt(json_encode($defaultdata),$key));
			if (substr($cookie,0,$contador)==substr($data,0,$contador) ){
				echo $data;
				echo " ";
				echo $key;
				echo " ";
				echo $contador;
				$temp[] = $key;
				echo "\n";
				$best_match = $key;
			}
		}
	}
	if($found_key == false){
		$first_candidates = $temp;
		$temp = [];
	}
	$contador++;
}

$defaultdata = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff");
echo  base64_encode(xor_encrypt(json_encode($defaultdata),$best_match));