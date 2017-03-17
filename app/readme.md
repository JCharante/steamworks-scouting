achilles app
============


## Development Setup

```
$ npm install cordova
$ cordova prepare
$ cordova run android
```

If you aren't using an emulator, then I recommend using [this](https://developers.google.com/web/tools/chrome-devtools/remote-debugging/?utm_source=dcc&utm_medium=redirect&utm_campaign=2016q3#debugging-webviews) to read console outputs.

To test non-phone features, you can simply open the local file as all imports are relative.

## Building Release

### 1. Create a keystore

```
keytool -genkey -v -keystore <keystoreName>.keystore -alias <Keystore AliasName> -keyalg <Key algorithm> -keysize <Key size> -validity <Key Validity in Days>
```

So for this example

```
 keytool -genkey -v -keystore JCharante.keystore -alias JCharante -keyalg RSA -keysize 2048 -validity 10000
```

and answer the prompts.

Files referenced will start from this folder. This file is `./readme.md`

Move a copy of your keystore (in this case, `JCharante.keystore`) to `platforms/android/build/outputs/apk/`.

(*.keystore is in the .gitignore so you don't have to worry about accidentally committing your .keystore file)

### 2. Generating the unsigned APK

```
$ cordova build --release android
```

The built file will be at `platforms/android/build/outputs/apk/android-release-unsigned.apk`

### 3. Signing the APK

Change your active directory into the one with your keystore & apk.

```
$ cd platforms/android/build/outputs/apk/
```

Now to sign it

```
$ jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore <keystorename <Unsigned APK file> <Keystore Alias name>
```

So in this case

```
$ jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore JCharante.keystore android-release-unsigned.apk JCharante
```

Follow the prompts and now it's signed.

One last thing, which is to use zipalign.

```
zipalign -v 4 android-release-unsigned.apk achilles-v1.0.4.0.apk
```

And we're done. Now you can upload it to a server for people to download or do stuff to get it on the app store.
