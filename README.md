# Price Alert Bot 🛍️

A Flask-based web application that tracks **Amazon product prices** and sends email alerts when prices drop below your target price.

## Features

- 📊 **Real-time Price Tracking** - Monitors Amazon product prices automatically
- 📧 **Email Alerts** - Get notified instantly via Gmail when prices drop
- 🎯 **Target Price Setting** - Set your desired price for any product
- 📱 **Responsive Dashboard** - View all tracked products in one place
- 📈 **Price History** - Automatic logging of price changes
- 🔄 **Auto-refresh** - Background worker checks prices every 30 seconds
- ✏️ **Easy Management** - Update target price or delete tracked products
- 🇮🇳 **Indian Currency Support** - Prices displayed in INR (₹)

## Technologies Used

- **Backend**: Flask (Python 3.8+)
- **Database**: MySQL
- **Web Scraping**: Selenium with Chrome WebDriver (headless mode)
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Email Service**: SMTP (Gmail)
- **Automation**: Threading for background price tracking

## Requirements

- Python 3.8 or higher
- MySQL Server
- Chrome Browser (for Selenium)
- Gmail account with App Password enabled

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kallamchinmayereddy/Price_alert_bot.git
cd Track-For-Me
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create a MySQL database and tables:

```sql
CREATE DATABASE price_tracker;
USE price_tracker;

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_name VARCHAR(255) NOT NULL,
  product_url TEXT NOT NULL,
  target_price DECIMAL(10,2) NOT NULL,
  email VARCHAR(255) NOT NULL,
  current_price DECIMAL(10,2),
  last_checked DATETIME,
  alert_sent BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE price_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  checked_at DATETIME NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
```

### 5. Environment Configuration

Create a `.env` file in the `Track-For-Me` directory with your database and email credentials:

```env
# MySQL Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=price_tracker

# Gmail SMTP (NOT your regular password)
EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
```

#### Setting Up Gmail App Password:
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Go to **App passwords**
4. Select "Mail" and "Windows Computer"
5. Copy the generated 16-character password
6. Use this password in `APP_PASSWORD` in your `.env` file

## Running the Application

### Start the Flask Server

```bash
cd Track-For-Me
python app.py
```

The application will be available at: **http://127.0.0.1:5000**

### What Happens:
- Flask server starts on port 5000
- Background thread automatically starts to track prices
- Prices are checked every **30 seconds**
- When a price drops to/below target, an email is sent automatically

## How to Use

### 1. Add a Product (Home Page)
- Go to `http://127.0.0.1:5000`
- Enter:
  - **Product Name**: Name of the item
  - **Amazon URL**: Full Amazon product link (e.g., `https://www.amazon.in/dp/ASIN...`)
  - **Target Price**: Price at which you want to be notified (in INR)
  - **Email**: Where you want to receive alerts
- Click **Start Tracking**

### 2. View Dashboard
- Go to `/dashboard` to see all tracked products
- Shows:
  - Current price
  - Target price
  - Last checked timestamp
  - Tracking status
  - Email address

### 3. Track Status
- **Tracking**: Waiting for price to drop
- **Alert Sent**: Price reached target, email was sent
- **Target Reached**: Current price ≤ target price

### 4. Manage Products
- **Edit**: Update target price or email
- **Delete**: Stop tracking a product

## Project Structure

```
Track-For-Me/
├── app.py                    # Main Flask application & routes
├── models.py                 # MySQL database operations
├── scraper.py                # Selenium Amazon price scraper
├── tracker.py                # Background price tracking worker
├── email_service.py          # Email notification service
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── static/
│   └── css/                  # Stylesheets
│       ├── main.css          # Main styles
│       ├── dashboard.css     # Dashboard specific styles
│       ├── result.css        # Result page styles
│       └── update.css        # Update form styles
└── templates/                # Jinja2 HTML templates
    ├── index.html            # Home page (add product)
    ├── result.html           # Product added confirmation
    ├── dashboard.html        # Dashboard view
    └── update.html           # Edit product page
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home page - Add new product |
| POST | `/track` | Submit new product to track |
| GET | `/dashboard` | View all tracked products |
| GET | `/update/<id>` | Edit product form |
| POST | `/update/<id>` | Update product target price/email |
| GET | `/delete/<id>` | Delete a product |

## How It Works

```
1. User adds product URL on home page
   ↓
2. Scraper fetches current Amazon price using Selenium
   ↓
3. Product stored in MySQL database
   ↓
4. Background thread (runs every 30 seconds):
   - Fetches all unalerted products
   - Scrapes latest price from Amazon
   - Updates database
   - Stores price history
   - If price ≤ target: Sends email & marks alert_sent
   ↓
5. User receives notification email
```

## Scraper Details

The scraper uses **Selenium with headless Chrome** to:
- Load Amazon product pages
- Wait for price elements to load (10 second timeout)
- Extract price from Amazon's price container
- Handle dynamic content loading

**Amazon-specific selectors used:**
- Price container: `corePriceDisplay_desktop_feature_div`
- Price whole: `.a-price-whole`
- Price fraction: `.a-price-fraction`

## Troubleshooting

### Issue: "Can't open named pipe to host"
**Solution**: 
- Ensure MySQL server is running
- Verify credentials in `.env` file
- Test connection: `mysql -u root -p`

### Issue: "No module named 'selenium'"
**Solution**:
```bash
pip install -r requirements.txt
```

### Issue: Prices not being tracked
**Check**:
- Verify Amazon URL is correct
- Check Chrome/Chromium is installed
- Look at terminal output for error messages
- Ensure `.env` file is in correct location

### Issue: Emails not being received
**Check**:
- Verify `APP_PASSWORD` is correct (not your Gmail password)
- Check spam folder
- Verify email address in database
- Test SMTP credentials manually

### Issue: "Chrome not found" or WebDriver errors
**Solution**:
- `webdriver-manager` should auto-download ChromeDriver
- If issues persist, ensure Chrome is installed: `choco install googlechrome` (Windows)
- Or: `brew install chromedriver` (macOS)

### Issue: "Price not found"
**Possible Causes**:
- Amazon page structure changed (selectors need updating)
- Product page has special pricing format
- Website is blocking Selenium automation
- Page took too long to load (timeout)

## Configuration & Customization

### Change Price Check Interval
Edit `tracker.py`, line with `time.sleep()`:
```python
time.sleep(30)  # Current: 30 seconds
# Change to:
time.sleep(60)  # For 60 seconds
```

### Modify Email Template
Edit `email_service.py` to customize the alert email:
```python
body = f"{product_name} is now at {price}"  # Modify this
```

### Add More E-commerce Sites
1. Update `scraper.py` to handle new URL formats
2. Find CSS selectors for price elements
3. Add conditional logic to detect website type
4. Test thoroughly before deploying

## Database Schema

### products table
```
- id: Primary Key (Auto-increment)
- product_name: Product name
- product_url: Amazon product URL
- target_price: Alert price (INR)
- email: Notification email
- current_price: Latest scraped price
- last_checked: Last price check timestamp
- alert_sent: Boolean (true if alert already sent)
```

### price_history table
```
- id: Primary Key (Auto-increment)
- product_id: Foreign Key (products.id)
- price: Price at time of check
- checked_at: Timestamp of price check
```

## Performance Notes

- **Selenium overhead**: ~5-10 seconds per scrape
- **30-second interval**: Good balance between accuracy and server load
- **Headless mode**: Faster than GUI browser
- **Threading**: Non-blocking background tracking

## Security Considerations

⚠️ **Important:**
- Never commit `.env` file to git
- Use Gmail App Passwords, not your actual password
- Keep database credentials secure
- Consider rate limiting on production

## Known Limitations

- Only works with Amazon.in product links
- Requires active internet connection
- Selenium scraping can be slow (5-10 seconds per product)
- Amazon may block automated requests (rate limiting)
- Price detection works with standard Amazon price format only

## Future Enhancements

- [ ] Support for Flipkart, Myntra, other e-commerce sites
- [ ] SMS alerts via Twilio
- [ ] Telegram bot notifications
- [ ] User authentication system
- [ ] Dark mode UI
- [ ] REST API for external integrations
- [ ] Price drop percentage alerts
- [ ] Scheduled email digests
- [ ] Admin dashboard for multiple users

## License

Open source project. Feel free to fork and modify!

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## Support

For bugs or questions:
- Open a GitHub issue: [Issues](https://github.com/kallamchinmayereddy/Price_alert_bot/issues)
- Check existing issues for solutions

---

**Happy Price Tracking!** 🎉 Save money by getting alerts for your favorite Amazon products!
