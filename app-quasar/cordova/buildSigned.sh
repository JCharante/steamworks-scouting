#!/usr/bin/env bash

mkdir -p builds

cordova build --release android

cd platforms/android/build/outputs/apk/

jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $ksf -storepass $ksp android-x86-release-unsigned.apk $ksa
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore $ksf -storepass $ksp android-armv7-release-unsigned.apk $ksa

touch achilles-$vnum-x86.apk
touch achilles-$vnum-armv7.apk

mv achilles-$vnum-x86.apk achilles-$vnum-x86.apk.old
mv achilles-$vnum-armv7.apk achilles-$vnum-armv7.apk.old

zipalign -v 4 android-x86-release-unsigned.apk achilles-$vnum-x86.apk
zipalign -v 4 android-armv7-release-unsigned.apk achilles-$vnum-armv7.apk

mv achilles-$vnum-x86.apk ../../../../../builds/
mv achilles-$vnum-armv7.apk ../../../../../builds/
