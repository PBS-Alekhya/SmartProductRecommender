
# Overview
The Smart Product Recommender is a machine learning-based system designed to recommend products based on user preferences. This project leverages Flask, Pandas, and Scikit-learn to provide content-based recommendations.

# Features
•	User Authentication: Register and log in securely.
•	Product Search: Users can search for a product to get recommendations.
•	Content-Based Filtering: Uses TF-IDF Vectorization and Cosine Similarity to suggest similar products.
•	Dynamic Recommendations: Displays images, ratings, and brands of suggested products.
•	Responsive UI: Built with HTML, CSS (Bootstrap), and JavaScript for a seamless experience.

# Technologies Used
•	Python (Flask, Pandas, Scikit-learn)
•	HTML, CSS, Bootstrap (Frontend UI)
•	SQLAlchemy (Database handling)
•	Jinja2 (For dynamic content rendering in templates)

# Project Structure
Smart Product Recommender/
│── static/
│   ├── assets/ (Product images and other static files)
│── templates/
│   ├── index.html (Landing Page)
│   ├── dashboard.html (Recommendation Page)
│── models/
│   ├── refined_data.csv (Preprocessed product data)
│── app.py (Main Flask application)
│── requirements.txt (Dependencies)
│── README.md (Project Documentation)

# How It Works
1.	User selects a product from the homepage.
2.	System analyzes product features using text-based similarities.
3.	Recommendations are displayed with product names, brands, images, and ratings.



