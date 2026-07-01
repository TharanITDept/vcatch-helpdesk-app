# VCATCH Helpdesk — Android App (Capacitor)

This folder wraps your existing VCATCH Helpdesk Portal (`www/index.html`) into a real native
Android app using Capacitor, ready to build and publish to the Google Play Store.

- **App Name:** VCATCH Helpdesk
- **Package ID (Application ID):** `in.vcatch.helpdesk`
- **Web code used:** exact copy of your current portal (`www/index.html`) — no changes needed.

---

## 1. What you need on your machine

- **Android Studio** (free): https://developer.android.com/studio
- **Node.js** (v18+): https://nodejs.org
- A **Google Play Developer account** ($25 one-time fee): https://play.google.com/console/signup

You do **not** need a Mac for Android (unlike iOS).

---

## 2. First-time setup

```bash
cd vcatch-app
npm install
npx cap sync android
npx cap open android
```

The last command opens the project in Android Studio. Let Gradle finish syncing
(first time can take a few minutes while it downloads the Android SDK components).

---

## 3. Add your app icon & splash screen (recommended before publishing)

Capacitor uses default placeholder icons right now. To brand it with the VCATCH logo:

1. Put a 1024×1024 PNG of your logo somewhere, e.g. `assets/icon.png`.
2. Install the asset generator:
   ```bash
   npm install @capacitor/assets --save-dev
   npx capacitor-assets generate --iconBackgroundColor '#0A0A0A' --splashBackgroundColor '#0A0A0A'
   ```
3. Re-sync: `npx cap sync android`

---

## 4. Test on a real device or emulator

In Android Studio: click the green ▶ Run button, pick a device/emulator.
The app should open showing your VCATCH login screen exactly as it looks on the web.

**Things worth testing specifically inside the app:**
- Login with EMP ID / phone + password
- Raising a ticket (Firestore write)
- Forgot Password → OTP email (EmailJS)
- Any WhatsApp/notification integrations you keep active

---

## 5. Build a release AAB (required by Play Store)

Google Play requires an **Android App Bundle (.aab)**, not a plain APK, for new apps.

1. In Android Studio: **Build → Generate Signed Bundle / APK → Android App Bundle**
2. Create a new **keystore** (first time only) — save this file and its passwords somewhere
   safe and permanent. If you lose it, you can never update this app again on Play Store.
3. Choose **release** build variant, finish the wizard.
4. Your signed `.aab` file appears under `android/app/release/`.

---

## 6. Publish on Google Play Console

1. Go to https://play.google.com/console, pay the one-time $25 registration fee if you
   haven't already.
2. **Create app** → fill in app name, default language, app/game type, free/paid.
3. Complete the required sections before you can release:
   - **App content**: Privacy policy URL (you'll need to host a simple privacy policy page —
     required since the app collects employee data), content rating questionnaire,
     target audience, data safety form (declare what data you collect: names, phone numbers,
     employee IDs, ticket descriptions — stored in Firebase).
   - **Store listing**: short & full description, app icon (512×512), feature graphic
     (1024×500), at least 2 phone screenshots.
4. Go to **Release → Production → Create new release**, upload the `.aab`, fill release notes.
5. Submit for review. Google typically reviews within a few hours to 1–2 days for the
   first submission.

> Since this is an **internal company tool**, you can alternatively publish it as an
> **Internal Testing** or **Closed Testing** release instead of full Production — this skips
> the public review queue and lets you share an install link with VCATCH employees only,
> without needing the full store listing polish.

---

## 7. Updating the app later

Whenever you change `www/index.html` (your portal code):

```bash
npx cap sync android
```

Then rebuild a new signed `.aab` (Step 5) with an **incremented version code** in
`android/app/build.gradle` (`versionCode` and `versionName`), and upload it as a new release
in Play Console.

---

## Notes specific to your portal

- Internet permission is already included by Capacitor by default — required since your
  app talks to Firebase Firestore, EmailJS, and any WhatsApp/push APIs.
- If you later replace WhatsApp notifications with native push (Firebase Cloud Messaging),
  that's an easy addition on top of this same project — just ask.
- Package ID `in.vcatch.helpdesk` is set for you; this **cannot be changed after your first
  Play Store upload**, so confirm it's what you want before publishing.
