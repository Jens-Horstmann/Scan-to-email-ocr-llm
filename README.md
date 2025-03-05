# Scan-to-email-ocr-llm

# Scan-to-Email Container Setup Guide

This guide will help you set up and run the **Scan-to-Email** container, which monitors a folder for scanned documents, extracts text using OCR, summarizes the content with an LLM, and sends an email with the extracted information.

## **1️⃣ Install Docker**
### **Windows & Mac:**
1. Download and install **Docker Desktop** from [Docker’s website](https://www.docker.com/products/docker-desktop/).
2. Follow the installation instructions and ensure Docker is running.

### **Linux (Ubuntu/Debian-based distributions):**
Run the following commands in the terminal:
```sh
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER  # Allow running Docker without sudo (log out and back in to apply)
```

Check that Docker is installed by running:
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

## **3️⃣ Set Up Two-Factor Authentication for Gmail (required for "app password")**
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
1. Open a terminal and run:
```sh
git clone https://github.com/Jens-Horstmann/scan-to-email-ocr-llm.git
cd scan-to-email
```
2. Create a new `.env` file:
```sh
nano .env
```
3. Add the following information (replace with your actual Gmail credentials and folder path):
```
SENDER_EMAIL=your-email@gmail.com
RECIPIENT_EMAIL=your-recipient@gmail.com
EMAIL_PASSWORD=your-app-password
MONITORED_FOLDER=/path/to/your/scans
```
4. Save the file (CTRL + X, then Y, then ENTER).

---

## **6️⃣ Build and Run the Container**
Run the following command to build and start the container:
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
  cp /path/to/test-file.pdf /path/to/your/scans/
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

