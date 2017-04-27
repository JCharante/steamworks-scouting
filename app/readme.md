achilles app
============


## View on Desktop

When you are working on something not related to QR encoding / QR scanning, you can simply use Chromium.

Just open the home/index.html file in Chromium.

For example, `file:///home/jcharante/Projects/achilles/app/www/compressionTest/index.html`

This also means you can view the current version in the master branch [here with rawgit.com](https://rawgit.com/JCharante/achilles/master/app/www/home/index.html)

## Android Development Setup

```
$ sudo apt install default-jdk gradle zipalign
$ npm install -g cordova
$ cordova prepare
$ cordova platform update android@6.2.1
$ cordova run android
```

If you aren't using an emulator, then I recommend using [this](https://developers.google.com/web/tools/chrome-devtools/remote-debugging/?utm_source=dcc&utm_medium=redirect&utm_campaign=2016q3#debugging-webviews) to read console outputs.

To test non-phone features, you can simply open the local file as all imports are relative.

## Building Releases

[This SO answer](http://stackoverflow.com/a/26450074/5006133) was adapted to suit our needs.

### 1. Create a keystore

```bash
$ keytool -genkey -v -keystore <keystoreName>.keystore -alias <Keystore AliasName> -keyalg <Key algorithm> -keysize <Key size> -validity <Key Validity in Days>
```

So for this example

```bash
$ keytool -genkey -v -keystore JCharante.keystore -alias JCharante -keyalg RSA -keysize 2048 -validity 10000
```

and answer the prompts.

Files referenced will start from this folder. This file is `./readme.md`

Move a copy of your keystore (in this case, `JCharante.keystore`) to `platforms/android/build/outputs/apk/`.

(*.keystore is in the .gitignore so you don't have to worry about accidentally committing your .keystore file)


### 2a. The Automated Way

You can use the bash script to automate the building, signing, and compression of the apk.

First set your environment variables

```bash
export "ksp=YOUR_KEY_STORE_PASSWORD"  # example: h@I#HROIJijfowi@#$%@fsG$33efUH3hur#R#~&
export vnum=APP_VERSION  # example v1.1.5.1
export ksf=KEY_STORE_FILE  # example: JCharante.keystore
export ksa=KEY_STORE_ALIAS  # example: JCharante
./buildSigned.sh
```

Your signed apk will available at `builds/achilles-$vnum.apk`

### 2b. Generating the unsigned APK

```bash
$ cordova build --release android
```

The built file will be at `platforms/android/build/outputs/apk/android-release-unsigned.apk`

### 3. Signing the APK

Change your active directory into the one with your keystore & apk.

```bash
$ cd platforms/android/build/outputs/apk/
```

Now to sign it

```bash
$ jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore <keystorename> <Unsigned APK file> <Keystore Alias name>
```

So in this case

```bash
$ jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore JCharante.keystore android-release-unsigned.apk JCharante
```

Follow the prompts and now it's signed.

One last thing, which is to use zipalign.

```bash
$ zipalign -v 4 android-release-unsigned.apk achilles-v1.0.4.0.apk
```

And we're done. Now you can upload it to a server for people to download or do stuff to get it on the app store.
