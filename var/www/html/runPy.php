<?php
{

      $uid = escapeshellcmd($_POST['timestamp']);

       exec("sudo python /var/www/scripts/appgenserver.py $uid");

      echo "http://45.55.58.149/release/".$uid."/releaseapk.apk";

}
?>

