# Track For Me - Price Tracker

A lightweight Flask app that monitors product prices on Amazon, Flipkart, and Myntra. When a product drops to your target price, you get an email. That's it.

## What You Get

- Track prices across 3 major Indian e-commerce platforms
- Automatic email alerts when prices hit your target
- Simple dashboard to manage tracked items
- Background worker runs every 30 seconds
- No BS, just working code

## Stack

- **Backend**: Flask
- **Database**: MySQL
- **Scraper**: Selenium (headless Chrome)
- **Email**: Gmail SMTP
- **Workers**: Threading

## Quick Start

### Prerequisites

- Python 3.8+
- MySQL Server
- Chrome (for Selenium)
- Gmail account

### Setup

1. **Clone and navigate**
```bash
git clone https://github.com/kallamchinmayereddy/Price_alert_bot.git
cd Track-For-Me
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux  
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up database**
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
  alert_sent BOOLEAN DEFAULT FALSE
);

CREATE TABLE price_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  checked_at DATETIME NOT NULL,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);
```

5. **Configure environment**

Create `.env` file:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=price_tracker
EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
```

**For Gmail**: Generate an App Password at https://myaccount.google.com/apppasswords (requires 2FA enabled). Use that, not your regular Gmail password.

6. **Run it**
```bash
python app.py
```

Open http://127.0.0.1:5000 and start tracking.

## How It Works

1. Add a product with URL (Amazon/Flipkart/Myntra), target price, and email
2. App scrapes current price immediately and stores it
3. Background thread checks all products every 30 seconds
4. When price ≤ target price, sends email and marks alert as sent
5. Edit or delete products from dashboard

## Supported URLs

- **Amazon**: `https://www.amazon.in/dp/ASIN` or full product URLs
- **Flipkart**: `https://www.flipkart.com/...` 
- **Myntra**: `https://www.myntra.com/...`

## Project Structure

```
Track-For-Me/
├── app.py              # Flask routes and app logic
├── scraper.py          # Selenium scrapers for each platform
├── tracker.py          # Background price checking thread
├── models.py           # Database operations
├── email_service.py    # Gmail SMTP handler
├── requirements.txt    # Dependencies
├── .env.example        # Environment template
├── static/css/         # Stylesheets
└── templates/          # HTML templates
```

## API Routes

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Home page - add new product |
| POST | `/track` | Submit product to track |
| GET | `/dashboard` | View all tracked products |
| GET/POST | `/update/<id>` | Edit product settings |
| GET | `/delete/<id>` | Remove product |

## Scraper Details

The scraper automatically detects which platform you're using based on URL and extracts price accordingly:

- **Amazon**: Looks for `corePriceDisplay_desktop_feature_div` and price elements
- **Flipkart**: Extracts from `._30jeq3` class
- **Myntra**: Pulls from `.discountedPriceText` class

Selenium runs in headless mode, which is fast and doesn't require display.

## Customization

### Change check interval
In `tracker.py`, modify the sleep time:
```python
time.sleep(30)  # Check every 30 seconds
```

### Modify email template
In `email_service.py`:
```python
body = f"{product_name} is now ₹{price}"
```

### Add a new e-commerce platform
1. Add scraper function in `scraper.py` (follow existing pattern)
2. Add URL detection in `get_price()`
3. Test with actual product links

## Troubleshooting

**"Can't connect to database"**
- Verify MySQL is running
- Check credentials in `.env`
- Run: `mysql -u root -p` to test

**"No module named 'selenium'"**
- Run: `pip install -r requirements.txt`

**Prices not updating**
- Check terminal for errors while app is running
- Verify product URLs are correct
- Website selectors may have changed (update scraper.py)

**Emails not arriving**
- Verify App Password is correct (not regular Gmail password)
- Check spam folder
- Ensure email in database is correct

**"Chrome not found"**
- `webdriver-manager` auto-downloads ChromeDriver
- If stuck, install Chrome manually or update ChromeDriver

**Website blocking Selenium**
- Sites detect automation and may return 403
- Selenium headers are obfuscated but some blocks are aggressive
- May need to add delays or try different selectors

## Database Schema

### products
- `id`: Auto-increment primary key
- `product_name`: Product name
- `product_url`: Full product URL
- `target_price`: Alert threshold
- `email`: Notification email
- `current_price`: Latest price scraped
- `last_checked`: Timestamp of last check
- `alert_sent`: True if alert already sent

### price_history
- `id`: Auto-increment primary key
- `product_id`: Foreign key to products
- `price`: Price at time of check
- `checked_at`: Timestamp

## Performance

- Scraping takes 5-10 seconds per product (depends on site responsiveness)
- 30-second check interval = good balance between accuracy and load
- Headless Chrome is much faster than full browser
- Threading doesn't block the web server
