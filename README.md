# This software (including this readme) is almost entirely written by ChatGPT-4o. Feel free to chat with it in case of any complaints. 
# This tool is specifically tuned to work well with scans or photos in German or English 

# Scan-to-Email Container Setup Guide

This guide will help you set up and run the **Scan-to-Email** container on **Windows**, which monitors a folder for scanned documents, extracts text using OCR, summarizes the content with an LLM, and sends an email with the extracted information.

## **1️⃣ Install Docker on Windows**
1. Download and install **Docker Desktop** from [Docker’s website](https://www.docker.com/products/docker-desktop/).
2. Follow the installation instructions and ensure Docker is running.
3. Open **Docker Desktop**, go to **Settings > Resources > WSL Integration**, and ensure your default WSL distribution is enabled.
4. Restart your computer to apply the changes.
5. Verify the installation by opening **Command Prompt (cmd)** or **PowerShell** and running:
   ```sh
   docker --version
   docker-compose --version
   ```

---

## **2️⃣ Create a New Gmail Address (Optional, Recommended for Security)**
If you want to keep your primary email secure, it is recommended to create a new Gmail account for sending scanned emails.

1. Go to [Google Account Signup](https://accounts.google.com/signup).
2. Follow the on-screen instructions to create a new Gmail address.

---

## **3️⃣ Set Up Two-Factor Authentication for Gmail**
1. Log in to your **Gmail account**.
2. Go to [Google Security Settings](https://myaccount.google.com/security).
3. Under **"How you sign in to Google"**, click **2-Step Verification** and follow the setup process.
4. Enable **Google Authenticator** or **another verification method**.

---

## **4️⃣ Create an App Password for Email Sending**
To allow the container to send emails without using your main password, you need to generate an **App Password**:

1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
2. Select **"Mail"** as the app and **"Other (Custom)"** for the device name (e.g., "Scan-to-Email").
3. Click **"Generate"** and copy the password displayed (you will not be able to see it again).

🚨 **Keep this password safe!** You will need it in the next step.

---

## **5️⃣ Clone the Repository and Configure the `.env` File**
1. Open **PowerShell** and navigate to your desired installation folder.
2. Clone the repository (if applicable):
   ```sh
   git clone https://github.com/Jens-Horstmann/scan-to-email-ocr-llm.git
   cd scan-to-email
   ```
   Or just download the repository into a folder
   
4. Create a new **`.env`** file:
   - Open **Notepad** and paste the following content:
     ```
     SENDER_EMAIL=your-email@gmail.com
     RECIPIENT_EMAIL=your-recipient@gmail.com
     EMAIL_PASSWORD=your-app-password
     MONITORED_FOLDER=C:\path\to\your\scans
     ```
   - Click **File > Save As**
   - In the **File name** box, type `.env` (with quotes) and save it in the project folder.

---

## **6️⃣ Build and Run the Container**
Run the following command in **PowerShell** to build and start the container:
```sh
docker-compose up -d --build
```

This will:
✅ Download all dependencies
✅ Set up OCR, email, and LLM services
✅ Start monitoring the specified folder

---

## **7️⃣ Testing and Troubleshooting**
- **Drop a scanned PDF/image into the monitored folder**:
  ```sh
  copy C:\path\to\test-file.pdf C:\path\to\your\scans
  ```
- **Check logs if emails are not sent**:
  ```sh
  docker-compose logs -f
  ```
- **Restart the container if needed**:
  ```sh
  docker-compose restart
  ```
- **Stop the container**:
  ```sh
  docker-compose down
  ```

🚀 Now, every scanned document in the monitored folder will be processed and sent via email! Let me know if you need additional setup assistance. 😊

