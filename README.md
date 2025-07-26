# NepalShop - E-Commerce Website

A complete e-commerce website built with Django featuring product catalog, shopping cart, checkout system, and payment integration with eSewa and Cash on Delivery (COD).

## Features

### 🛒 Core E-Commerce Features
- **Product Catalog**: Browse products with categories, search, and filtering
- **Shopping Cart**: Add/remove items, update quantities
- **Checkout Process**: Complete order placement with customer information
- **Order Management**: Order history and status tracking
- **User Authentication**: Admin panel access and customer accounts

### 💳 Payment Methods
- **eSewa Integration**: Digital wallet payment for online transactions
- **Cash on Delivery (COD)**: Pay when your order is delivered
- **Payment Status Tracking**: Real-time payment confirmation

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **Interactive Elements**: AJAX-powered cart updates
- **Professional Styling**: Clean and modern design with Font Awesome icons
- **User-Friendly Navigation**: Intuitive browsing experience

### 📊 Admin Features
- **Django Admin Panel**: Complete product and order management
- **Inventory Management**: Stock tracking and updates
- **Customer Management**: Customer information and order history
- **Payment Tracking**: Monitor payment statuses and methods

## Technology Stack

- **Backend**: Django 5.2.4 + Django REST Framework
- **Database**: SQLite (development) / MySQL (production)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript, jQuery
- **Payment**: eSewa Payment Gateway Integration
- **Media Handling**: Pillow for image processing

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone the Repository
```bash
git clone <repository-url>
cd workspace
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Populate Sample Data
```bash
python populate_data.py
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the website.

## Usage

### Customer Features
1. **Browse Products**: Visit the homepage to see featured products and categories
2. **Search & Filter**: Use the search bar and category filters to find products
3. **Add to Cart**: Click "Add to Cart" on any product
4. **Checkout**: Proceed through the checkout process with customer information
5. **Payment**: Choose between eSewa or Cash on Delivery
6. **Order Tracking**: View order history and status (requires login)

### Admin Features
1. **Access Admin Panel**: Go to `/admin/` and login with superuser credentials
2. **Manage Products**: Add, edit, or remove products and categories
3. **Process Orders**: Update order statuses and manage customer orders
4. **Monitor Payments**: Track payment statuses and transaction details

## Project Structure

```
workspace/
├── app/                    # Main Django application
│   ├── models.py          # Database models (Product, Order, Cart, etc.)
│   ├── views.py           # View functions for web pages
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin panel configuration
│   ├── api/               # REST API endpoints
│   └── migrations/        # Database migrations
├── core/                  # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI configuration
├── templates/app/         # HTML templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── populate_data.py       # Sample data script
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## Database Models

### Core Models
- **Category**: Product categories
- **Product**: Product information with pricing and stock
- **Customer**: Customer information and profiles
- **Cart & CartItem**: Shopping cart functionality
- **Order & OrderItem**: Order management
- **Payment**: Payment tracking and status

## Payment Integration

### eSewa Configuration
The project is configured to work with eSewa's test environment. For production:

1. Update `ESEWA_MERCHANT_ID` in settings.py
2. Change eSewa URL from UAT to production
3. Implement proper payment verification

### Adding New Payment Methods
1. Add payment method to `Payment.PAYMENT_METHOD_CHOICES`
2. Create payment processing logic in `checkout` view
3. Add payment option to checkout template

## API Endpoints

The project includes REST API endpoints for:
- `/api/event-list/` - User management (legacy)
- Cart management (AJAX endpoints)
- Payment processing

## Security Features

- CSRF protection on all forms
- User authentication for order history
- Secure payment handling
- Input validation and sanitization

## Deployment

### For Production
1. Change `DEBUG = False` in settings.py
2. Set up proper database (MySQL/PostgreSQL)
3. Configure static file serving
4. Set up proper eSewa merchant account
5. Configure email settings for order notifications
6. Set up SSL certificate for secure payments

### Environment Variables
Create a `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
ESEWA_MERCHANT_ID=your-merchant-id
```

## Sample Data

The project includes a script to populate the database with sample data:
- 6 product categories (Electronics, Clothing, Books, etc.)
- 20 sample products with realistic pricing
- Proper stock quantities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support and questions:
- Email: admin@nepalshop.com
- Phone: +977-1-4444444

## License

This project is created for educational and demonstration purposes.

---

**Admin Credentials:**
- Username: `admin`
- Password: `admin123`

**Test eSewa Credentials:**
- Use eSewa's test environment credentials for testing payments
- The site is configured to work with eSewa's UAT environment