#!/usr/bin/env bash

mkdir -p builds

cordova build --release android

cd platforms/android/build/outputs/apk/

jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $ksf -storepass $ksp android-release-unsigned.apk $ksa

touch achilles-$vnum.apk

mv achilles-$vnum.apk achilles-$vnum.apk.old

zipalign -v 4 android-release-unsigned.apk achilles-$vnum.apk

mv achilles-$vnum.apk ../../../../../builds/
