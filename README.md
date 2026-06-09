# Price Alert Bot 🛍️

A Flask-based web application that tracks product prices from e-commerce websites and sends email alerts when prices drop below your target price.

## Features

- 📊 **Real-time Price Tracking** - Continuously monitors product prices
- 📧 **Email Alerts** - Get notified instantly when prices drop
- 🎯 **Target Price Setting** - Set your desired price for any product
- 📱 **Responsive Dashboard** - View all tracked products in one place
- 📈 **Price History** - Track price changes over time
- 🔄 **Auto-refresh** - Background worker checks prices every 60 seconds
- ✏️ **Easy Management** - Update or delete tracked products anytime

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: MySQL
- **Web Scraping**: BeautifulSoup, Requests
- **Frontend**: HTML, CSS, Jinja2 Templates
- **Email**: SMTP (Gmail)

## Prerequisites

- Python 3.8+
- MySQL Server
- Gmail account (for email alerts)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kallamchinmayereddy/Price_alert_bot.git
cd Track-For-Me
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Additional packages:
```bash
pip install mysql-connector-python python-dotenv
```

### 4. Database Setup

Create a MySQL database:

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

Create a `.env` file in the `Track-For-Me` directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=price_tracker

EMAIL=your_email@gmail.com
APP_PASSWORD=your_gmail_app_password
```

**Gmail Setup**:
- Enable 2-Factor Authentication on your Gmail account
- Generate an [App Password](https://myaccount.google.com/apppasswords)
- Use the generated password in `APP_PASSWORD`

## Running the Application

```bash
cd Track-For-Me
python app.py
```

The application will be available at: `http://127.0.0.1:5000`

## Usage

1. **Home Page** (`/`) - Add a new product to track
   - Enter product name
   - Paste product URL
   - Set your target price
   - Provide your email

2. **Dashboard** (`/dashboard`) - View all tracked products
   - See current prices
   - Track status
   - Edit or delete products

3. **Update Product** (`/update/<product_id>`) - Modify price or email
   - Change target price
   - Update alert email

4. **Auto Tracking**
   - Background worker checks prices every 60 seconds
   - Email alert sent when price ≤ target price

## Project Structure

```
Track-For-Me/
├── app.py                 # Main Flask application
├── models.py              # Database operations
├── scraper.py             # Web scraping logic
├── tracker.py             # Background price tracking
├── email_service.py       # Email notification service
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── static/
│   └── css/               # Stylesheets
│       ├── main.css
│       ├── dashboard.css
│       ├── result.css
│       └── update.css
└── templates/             # HTML templates
    ├── index.html         # Home page
    ├── result.html        # Product added confirmation
    ├── dashboard.html     # Dashboard view
    └── update.html        # Edit product page
```

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | Home page |
| POST | `/track` | Add new product |
| GET | `/dashboard` | View all products |
| GET/POST | `/update/<id>` | Update product |
| GET | `/delete/<id>` | Delete product |

## Configuration

### Supported Websites

Currently supports price scraping from:
- Myntra
- Flipkart
- Amazon (and other e-commerce sites with standard HTML structure)

### Customizing Scraper

Edit `scraper.py` to add support for more websites.

## Troubleshooting

### Issue: "Can't open named pipe to host"
- Ensure MySQL server is running
- Check database credentials in `.env`

### Issue: Email not sending
- Verify Gmail App Password is correct
- Enable "Less secure app access" if using regular password
- Check spam folder

### Issue: No prices being tracked
- Verify website selector in `scraper.py` matches the site's HTML
- Check browser console for CSS selectors

## Future Enhancements

- [ ] Support for more e-commerce sites
- [ ] SMS alerts
- [ ] Telegram notifications
- [ ] Price drop percentage alerts
- [ ] User authentication
- [ ] Dark mode UI
- [ ] API for external integrations

## License

This project is open source. Feel free to fork and modify!

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions, please open a GitHub issue.

---

**Happy Price Tracking!** 🎉
