from flask import Flask, request, render_template
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

web_app = Flask(__name__)

# ===========================================================================================================
popular_products = pd.read_csv("models/popular_products.csv")
processed_data = pd.read_csv("models/refined_data.csv")

# ----------------------------------------------------------------------------------------------------------
web_app.secret_key = "randomsecurekey123"
web_app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/product_recommender"
web_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_instance = SQLAlchemy(web_app)


class UserRegistration(db_instance.Model):
    user_id = db_instance.Column(db_instance.Integer, primary_key=True)
    user_name = db_instance.Column(db_instance.String(100), nullable=False)
    user_email = db_instance.Column(db_instance.String(100), nullable=False)
    user_password = db_instance.Column(db_instance.String(100), nullable=False)

class UserLogin(db_instance.Model):
    login_id = db_instance.Column(db_instance.Integer, primary_key=True)
    login_name = db_instance.Column(db_instance.String(100), nullable=False)
    login_password = db_instance.Column(db_instance.String(100), nullable=False)


# ============================================================================================
def shorten_text(content, max_length):
    return content[:max_length] + "..." if len(content) > max_length else content


def generate_recommendations(processed_data, product_name, top_n=10):
    if product_name not in processed_data['ProductTitle'].values:
        return pd.DataFrame()
    
    tfidf_processor = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_processor.fit_transform(processed_data['ProductTags'])
    similarity_scores = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    product_index = processed_data[processed_data['ProductTitle'] == product_name].index[0]
    ranked_products = sorted(list(enumerate(similarity_scores[product_index])), key=lambda x: x[1], reverse=True)
    
    top_similar_indices = [x[0] for x in ranked_products[1:top_n+1]]
    recommended_products = processed_data.iloc[top_similar_indices][['ProductTitle', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]
    
    return recommended_products

# ===============================================================================
image_paths = [
    "static/assets/img_1.png", "static/assets/img_2.png", "static/assets/img_3.png",
    "static/assets/img_4.png", "static/assets/img_5.png", "static/assets/img_6.png",
    "static/assets/img_7.png", "static/assets/img_8.png"
]


@web_app.route("/")
def homepage():
    randomized_images = [random.choice(image_paths) for _ in range(len(popular_products))]
    price_list = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_items=popular_products.head(8), shorten_text=shorten_text,
                           randomized_images=randomized_images, chosen_price=random.choice(price_list))

@web_app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@web_app.route("/user_register", methods=['POST','GET'])
def user_register():
    if request.method == 'POST':
        user_name = request.form['username']
        user_email = request.form['email']
        user_password = request.form['password']
        
        new_user = UserRegistration(user_name=user_name, user_email=user_email, user_password=user_password)
        db_instance.session.add(new_user)
        db_instance.session.commit()
        
        randomized_images = [random.choice(image_paths) for _ in range(len(popular_products))]
        price_list = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html', trending_items=popular_products.head(8), shorten_text=shorten_text,
                               randomized_images=randomized_images, chosen_price=random.choice(price_list),
                               user_message='Registration successful!')


@web_app.route("/user_login", methods=['POST', 'GET'])
def user_login():
    if request.method == 'POST':
        login_name = request.form['signinUsername']
        login_password = request.form['signinPassword']
        
        new_login = UserLogin(login_name=login_name, login_password=login_password)
        db_instance.session.add(new_login)
        db_instance.session.commit()
        
        randomized_images = [random.choice(image_paths) for _ in range(len(popular_products))]
        price_list = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
        return render_template('index.html', trending_items=popular_products.head(8), shorten_text=shorten_text,
                               randomized_images=randomized_images, chosen_price=random.choice(price_list),
                               user_message='Login successful!')


@web_app.route("/get_recommendations", methods=['POST', 'GET'])
def get_recommendations():
    if request.method == 'POST':
        search_product = request.form.get('prod')
        num_recommendations = int(request.form.get('nbr'))
        recommended_items = generate_recommendations(processed_data, search_product, top_n=num_recommendations)
        
        if recommended_items.empty:
            return render_template('dashboard.html', message="No recommendations found for this product.")
        else:
            randomized_images = [random.choice(image_paths) for _ in range(len(popular_products))]
            price_list = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
            return render_template('dashboard.html', recommended_items=recommended_items, shorten_text=shorten_text,
                                   randomized_images=randomized_images, chosen_price=random.choice(price_list))


if __name__ == '__main__':
    web_app.run(debug=True)
