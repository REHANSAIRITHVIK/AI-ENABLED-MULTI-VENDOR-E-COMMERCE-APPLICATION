##AI ENABLED-MULTI-VENDOR-E-COMMERCE-APPLICATION

🚀 AI-Enabled Multi-Vendor E-Commerce Marketplace
An advanced, full-stack marketplace designed for the modern web. This application features a robust Multi-Vendor Architecture, AI-driven insights, and a high-performance Obsidian Dark UI for a premium user experience.

🌟 Key Features

🤖 AI Integration
1. Smart Product Recommendations:
Dynamically suggests items based on user browsing patterns and categories.
2. Predictive Stock Alerts: 
Uses real-time data to warn vendors of low inventory before they run out.
3. Automated Pricing Insights: Helps vendors understand market trends within their dashboard.

🏪 Multi-Vendor Ecosystem
1. Dedicated Vendor Dashboards: 
Independent control panels for inventory management and order processing.
2. Admin Command Center:
Global oversight of all users, products, and platform health.
3. Role-Based Access Control (RBAC):
Secure separation between Customers, Vendors, and Administrators.

🎨 Premium UI/UX
1. Obsidian & Neon Design:
A "No-White" interface using high-contrast neon accents (Cyan, Purple, Pink).
2. FOMO Implementation:
Real-time "Low Stock" and "Active Viewer" alerts to drive conversions.
3. Responsive Grid System: 
Compact, mobile-friendly product displays modeled after industry leaders like Flipkart.

🛠️ Tech StackLayerTechnology
Backend		:		Python / Flask
Database	:		SQLite3 (Relational)
Frontend	:		HTML5, CSS3 (Custom Glassmorphism), JavaScript
Styling		:		Custom Modular CSS (Obsidian Theme)
Security	:		Flask-Session, Password Hashing

📂 Project Structure

AI-ENABLED-MULTI-VENDOR-E-COMMERCE-APPLICATION/
│
├── app.py                      # Core Application: Flask routes, Business logic, & SQLAlchemy models
├── requirements.txt            # Project Dependencies: Flask, Flask-SQLAlchemy, Werkzeug, etc.
├── README.md                   # Project Documentation and Setup Instructions
│
├── instance/
│   └── ecommerce.db            # SQLite Database (Auto-generated on first run)
│
├── static/                     # Global Static Assets
│   ├── css/                    # Modular Stylesheets
│   │   ├── main.css            # Global theme (Dark mode / Typography)
│   │   ├── auth.css            # Authentication (Login/Register) UI
│   │   ├── customer.css        # Customer Dashboard components
│   │   ├── vendor.css          # Vendor-specific management UI
│   │   ├── admin.css           # Administrative control panel styles
│   │   ├── product.css         # Product cards, cart, and checkout styling
│   │   └── sidebar.css         # Amazon-style navigation/filter panel
│   │
│   ├── js/                     # Client-side Logic
│   │   ├── search.js           # Dynamic search & autocomplete
│   │   ├── cart.js             # Cart CRUD operations (Add/Remove/Update)
│   │   ├── filters.js          # Sidebar filtering logic (Category, Price, Rating)
│   │   ├── slider.js           # Product image gallery & carousel
│   │   ├── dashboard.js        # Analytics charts & UI interactions
│   │   └── location_lang.js    # Geolocation & Language localization
│   │
│   └── images/                 # Organized Product Image Repository
│       ├── laptops/            │   ├── books/
│       ├── mobiles/            │   ├── watches/ (mens/womens)
│       ├── tv/                 │   ├── headphones/
│       ├── ac/                 │   ├── mens_fashion/ (tshirts/shirts/jeans)
│       ├── refrigerator/       │   └── womens_fashion/
│       └── shoes/ (mens/womens)
│
└── templates/                  # Jinja2 HTML Templates
    ├── shared/                 # Reusable UI Components
    │   ├── base.html           # Main Layout Wrapper
    │   ├── navbar.html         # Role-based Header (Admin/Vendor/Customer)
    │   ├── sidebar.html        # Contextual Filter Sidebar
    │   └── footer.html         # Site Footer
    │
    ├── auth/                   # Identity Management
    │   ├── login.html          # User Login Page
    │   └── register.html       # User Registration Page
    │
    ├── customer/               # Customer-Facing Views
    │   ├── dashboard.html      # Personalized Home / Categories
    │   ├── view_products.html  # Product Listings
    │   ├── product.html        # Detailed Product View
    │   ├── cart.html           # Shopping Cart Summary
    │   ├── checkout.html       # Shipping & Order Review
    │   ├── payments.html       # Payment Gateway Integration
    │   ├── orders.html         # Purchase History
    │   └── profile.html        # Account Settings
    │
    ├── vendor/                 # Merchant Dashboard
    │   ├── dashboard.html      # Sales overview & stats
    │   ├── add_product.html    # Inventory Management (Insert)
    │   ├── view_products.html  # Inventory Management (List)
    │   └── orders.html         # Incoming Order Management
    │
    └── admin/                  # System Administration
        ├── dashboard.html      # Site-wide Analytics
        ├── categories.html     # Category Management
        ├── products.html       # Product Moderation
        └── customers.html      # User Base Management
		
🚀 Installation & Setup

1. Clone the repository
https://github.com/REHANSAIRITHVIK/AI-ENABLED-MULTI-VENDOR-E-COMMERCE-APPLICATION.git
CD AI-ENABLED-MULTI-VENDOR-E-COMMERCE-APPLICATION

2. Install Dependencies
pip install flask

3. Initialize the Database
The application automatically generates ecommerce.db on the first run.

4. Run the Application
python app.py

Access the app at http://127.0.0.1:5000


📸 Dashboard Previews
Note: The UI uses a "No-White" policy, utilizing #050505 backgrounds with #00f2ff (Cyan) for Customers and #bc13fe (Purple) for Vendors.

Auth Page: Featuring massive, glowing login containers for high conversion.

Vendor Panel: Real-time sales tracking with high-contrast data visualization.

Product Cards: Compact, elegant cards with "Low Stock" FOMO badges.


💡 Future Roadmap
[ ] Integration with Stripe/Razorpay API.

[ ] Image recognition for AI-based product tagging.

[ ] Real-time Chat between Customers and Vendors.


🧑‍💻 Developed By
👨‍💻 DASIKA REHAN SAI RITHVIK

B.Sc. (Hons) in Computer Science – Nizam College Autonomous (Osmania University)
Email: rehansairithvikdasika@gmail.com
Mobile Number: 9581277713