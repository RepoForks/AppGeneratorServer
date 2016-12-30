#!/bin/bash

#Change to new folder
cd $1

pwd
cd ./open-event-android/android
echo "Start building apk"
#chmod -R 777 $1/open-event-android/android/.gradle/2.11/
export ANDROID_HOME=/var/www/android-sdk-linux/
./gradlew assembleRelease --info
jarsigner -keystore /var/www/release-key.keystore -storepass fossasia app/build/outputs/apk/app-googleplay-release-unsigned.apk fossasia
/var/www/android-sdk-linux/build-tools/24.0.1/zipalign -v 4 app/build/outputs/apk/app-googleplay-release-unsigned.apk releaseapk.apk
echo "done"
