# 🛒 Python Role-Based Inventory System

A robust, command-line interface (CLI) application for managing users and inventory. This system features a dual-dashboard design for **Admins** and **Customers**, utilizing JSON files for persistent data storage.

## Key Features

### User Management
- **Secure Registration:** Validates emails via Regex and enforces strong password policies.
- **Role-Based Login:** Automatically directs users to either the Admin or User dashboard.
- **Profile Management:** Users can update their username, email, or password.

### Inventory & Admin Tools
- **Full CRUD Operations:** Admins can Create, Read, Update, and Delete products.
- **Stock Tracking:** Real-time quantity updates when products are purchased.
- **User Oversight:** Admins can view all registered users or delete specific accounts.

### Customer Experience
- **Product Discovery:** View all products or search by Name/ID.
- **Purchase System:** Validates stock levels before allowing a purchase.
- **Order History:** Users can view a list of all items they have bought.

## Tech Stack
- **Language:** Python 3.x
- **Storage:** JSON (Local File Database)
- **Libraries:** `json`, `re`, `pathlib`

## Getting Started

### Prerequisites
- Python 3.10 or higher installed.

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Nejat-33/Inventory-Management-Python.git](https://github.com/Nejat-33/Inventory-Management-Python.git)
2. Run the Application:
   python "advanced python.py"
