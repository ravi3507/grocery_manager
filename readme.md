Grocery Store Manager

Grocery Store Manager is a web application built with Flask that allows users to manage products, categories, and a simple shopping cart. This README provides an overview of the app's features and instructions on how to run it.


Getting Started
To run this application locally or deploy it on a server, follow these steps:

Clone the repository to your local machine:

Install the required dependencies by navigating to the project directory and running:
pip install -r requirements.txt

Start the Flask development server:
python app.py

Open a web browser and access the app at http://localhost:5000.

Features
User Authentication: The app supports user authentication with different roles (admin and user).

Product Management: Admin users can add, edit, and remove products with details such as name, price, quantity, category, and unit.

Category Management: Admin users can create, edit, and delete product categories.

Shopping Cart: Users can add products to their shopping cart, view the cart contents, and proceed to checkout.

Search Functionality: Users can search for products or categories by name.

User Roles
Manager: Managers have access to the managers's dashboard, where they can manage products and categories.

Customer: Regular customers can browse products, add them to the cart, and make purchases.

Usage
Manager Login:

Visit http://localhost:5000/admin to access the manager login page.
Use the following admin credentials:
Username: manager@gmail.com
Password: manager@123

Customer Login:

Visit http://localhost:5000/user to access the user login page.
Use the following user credentials:
Username: customer@gmail.com
Password: customer@123

Manager Dashboard:

Once logged in as an manager, you can manage categories and products from the manger dashboard.
User Dashboard:

After logging in as a customer, you can browse products, search for items, and add them to your shopping cart.
Shopping Cart:

Visit http://localhost:5000/user/cart to view and manage your shopping cart.

Checkout:
Proceed to the checkout page to complete your purchase.

License
This project is licensed under the MIT License.

