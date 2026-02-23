# College Chatbot - MongoDB Setup Guide

## Database Integration

Your chatbot now uses **MongoDB** to store FAQs and program information instead of hardcoding them.

## Setup Instructions

### Option 1: Local MongoDB (Windows)

1. **Download MongoDB Community Edition**
   - Visit: https://www.mongodb.com/try/download/community
   - Download MongoDB Community Server for Windows

2. **Install MongoDB**
   - Run the installer
   - Follow the setup wizard
   - MongoDB will be installed and run as a Windows Service

3. **Verify Installation**
   - Open Command Prompt and run:
   ```
   mongosh
   ```
   - If it connects, you're good to go!

4. **Start Your Chatbot**
   ```
   python project.py
   ```
   - The database will automatically initialize with sample data

### Option 2: MongoDB Atlas (Cloud) - Recommended for Production

1. **Create Free Account**
   - Go to: https://www.mongodb.com/cloud/atlas
   - Sign up for a free account
   - Create a new project

2. **Create a Cluster**
   - Click "Create a Cluster"
   - Choose "Free" tier
   - Select your region
   - Click "Create Cluster"

3. **Get Connection String**
   - Go to Clusters > Connect
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password

4. **Set Environment Variable**
   - Windows (PowerShell):
   ```
   $env:MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
   ```
   - Or add to your system environment variables permanently

5. **Start Your Chatbot**
   ```
   python project.py
   ```

## Database Structure

### FAQs Collection
```
{
  "q": "What programs are offered?"
}
```

### Programs Collection
```
{
  "name": "Bachelor's of Computer Applications",
  "category": "Undergraduate",
  "duration": "3 Years",
  "eligibility": "10+2 with Mathematics",
  "fees": "₹45,000 per year",
  "seats": "60"
}
```

## Using the Database

### In Python Code

```python
from database import get_faqs, get_programs, add_faq, add_program

# Get all FAQs
faqs = get_faqs()

# Get all programs
programs = get_programs()

# Add new FAQ
add_faq("How to apply for scholarships?")

# Add new program
add_program(
    name="Bachelor's of Arts",
    category="Undergraduate",
    duration="3 Years",
    eligibility="10+2",
    fees="₹30,000 per year",
    seats="100"
)
```

## Troubleshooting

**Error: "Failed to connect to MongoDB"**
- Make sure MongoDB is running
- Check your connection string
- Verify MONGO_URI environment variable

**Error: "Connection timeout"**
- If using MongoDB Atlas, check your IP whitelist
- Add your IP address to the cluster access list

**Database not initializing**
- Delete existing collections and restart the app
- Check MongoDB logs for errors

## Next Steps

Once MongoDB is set up and working:
- You can add/update FAQs without restarting the code
- Build an admin dashboard to manage programs
- Track chat analytics in MongoDB
- Scale to multiple servers easily

Questions? Let me know!
