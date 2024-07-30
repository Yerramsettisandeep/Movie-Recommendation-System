import streamlit as st
import pandas as pd
import requests
import bs4 as bs
import pickle
import json
import base64

# Function to inject CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to set background image
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpeg;base64,{encoded_image}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

local_css("static/style.css")

# Load movie data and similarity
movies = pickle.load(open('models/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies)
similarity = pickle.load(open('models/similarity.pkl', 'rb'))

# Path to the users.json file
USER_FILE_PATH = 'users.json'
ACTIVITY_FILE_PATH = 'user_activity.csv'
REVIEW_FILE_PATH = 'reviews.csv'
WATCHLIST_FILE_PATH = 'watchlist.csv'

# Load user data
def load_users():
    with open(USER_FILE_PATH, 'r') as f:
        return json.load(f)

# Save user data
def save_users(users):
    with open(USER_FILE_PATH, 'w') as f:
        json.dump(users, f)

# Load user activity
def load_activity():
    try:
        return pd.read_csv(ACTIVITY_FILE_PATH)
    except FileNotFoundError:
        return pd.DataFrame(columns=['username', 'action', 'details'])

# Save user activity
def save_activity(activity):
    activity.to_csv(ACTIVITY_FILE_PATH, index=False)

# Load reviews from a file
def load_reviews():
    try:
        return pd.read_csv(REVIEW_FILE_PATH)
    except FileNotFoundError:
        return pd.DataFrame(columns=['username', 'movie_title', 'review'])

# Save reviews to a file
def save_reviews(reviews):
    reviews.to_csv(REVIEW_FILE_PATH, index=False)

# Load watchlist from a file
def load_watchlist():
    try:
        return pd.read_csv(WATCHLIST_FILE_PATH)
    except FileNotFoundError:
        return pd.DataFrame(columns=['username', 'movie_title'])

# Save watchlist to a file
def save_watchlist(watchlist):
    watchlist.to_csv(WATCHLIST_FILE_PATH, index=False)

# Initialize session state for user management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'is_superuser' not in st.session_state:
    st.session_state.is_superuser = False

# Function to fetch movie posters
def fetch_poster(movie_name):
    searchLink = "https://www.bing.com/images/search?q=" + movie_name.replace(" ", "+") + "+movie+poster"
    page = requests.get(searchLink)
    soup = bs.BeautifulSoup(page.content, 'html.parser')
    elements = soup.find_all('img', class_='mimg')
    if elements:
        imgLink = elements[0].get('src')
        return imgLink
    return None

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_name = movies.iloc[i[0]].title
        recommended_movie_posters.append(fetch_poster(movie_name))
        recommended_movie_names.append(movie_name)
    return recommended_movie_names, recommended_movie_posters

# Load ratings from a file
def load_ratings():
    try:
        return pd.read_csv('ratings.csv')
    except FileNotFoundError:
        return pd.DataFrame(columns=['username', 'movie_title', 'rating'])

# Save ratings to a file
def save_ratings(ratings):
    ratings.to_csv('ratings.csv', index=False)

# Login and Registration
def login(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.is_superuser = user.get('is_superuser', False)
            st.success("Logged in successfully!")
            return
    st.error("Invalid username or password")

def register(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username:
            st.error("Username already exists")
            return
    users.append({"username": username, "password": password, "is_superuser": False})
    save_users(users)
    st.success("User registered successfully")

def create_superuser(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username:
            st.error("Superuser username already exists")
            return
    users.append({"username": username, "password": password, "is_superuser": True})
    save_users(users)
    st.success("Superuser created successfully")

def record_activity(username, action, details):
    activity = load_activity()
    new_entry = pd.DataFrame([{
        'username': username,
        'action': action,
        'details': details
    }])
    activity = pd.concat([activity, new_entry], ignore_index=True)
    save_activity(activity)

def show_movie_details(movie_name):
    # Check if movie exists
    if movie_name not in movies['title'].values:
        st.error(f"No details found for movie '{movie_name}'")
        return

    movie_details = movies[movies['title'] == movie_name].iloc[0]

    st.write(f"*Title:* {movie_details.get('title', 'N/A')}")
    st.write(f"*Overview:* {movie_details.get('overview', 'Overview not available')}")

    poster_url = fetch_poster(movie_name)
    if poster_url:
        st.image(poster_url, use_column_width=True)

    # Display ratings
    ratings = load_ratings()
    movie_ratings = ratings[ratings['movie_title'] == movie_name]
    if not movie_ratings.empty:
        st.subheader("Ratings")
        for _, row in movie_ratings.iterrows():
            st.write(f"*Username:* {row['username']} - *Rating:* {row['rating']}")
    else:
        st.write("No ratings yet for this movie.")

    # Display reviews
    reviews = load_reviews()
    movie_reviews = reviews[reviews['movie_title'] == movie_name]
    if not movie_reviews.empty:
        st.subheader("Reviews")
        for _, row in movie_reviews.iterrows():
            st.write(f"*Username:* {row['username']}")
            st.write(f"*Review:* {row['review']}")
    else:
        st.write("No reviews yet for this movie.")

# Watchlist functionality
def add_to_watchlist(username, movie_title):
    watchlist = load_watchlist()
    if not ((watchlist['username'] == username) & (watchlist['movie_title'] == movie_title)).any():
        new_entry = pd.DataFrame([{
            'username': username,
            'movie_title': movie_title
        }])
        watchlist = pd.concat([watchlist, new_entry], ignore_index=True)
        save_watchlist(watchlist)
        st.success(f"'{movie_title}' added to your watchlist")
    else:
        st.info(f"'{movie_title}' is already in your watchlist")

def view_watchlist(username):
    watchlist = load_watchlist()
    user_watchlist = watchlist[watchlist['username'] == username]
    if not user_watchlist.empty:
        st.subheader("Your Watchlist")
        for _, row in user_watchlist.iterrows():
            st.write(row['movie_title'])
    else:
        st.write("Your watchlist is empty")

def main():
    st.title("Movie Recommendation System")

    # Sidebar for navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Home", "About", "Movie Recommender", "User History", "Feedback", "Help"])

    if page == "Home":
        set_background("static/background_home.jpg")
        st.write("""
        Welcome to the Movie Recommendation System. Use the sidebar to navigate through different pages.
        """)

    elif page == "About":
        set_background("static/background_about.jpg")
        st.write("""
        The Movie Recommendation System helps users discover new movies based on their preferences. 
        - *Home*: Overview of the app.
        - *About*: Details about the app.
        - *Movie Recommender*: Get movie recommendations and rate movies.
        - *User History*: View your search and rating history.
        - *Feedback*: Provide your feedback about the app.
        - *Help*: Instructions on how to use the app.
        """)

    elif page == "Movie Recommender":
        set_background("static/background_recommender.jpg")
        st.header('Movie Recommender')

        if not st.session_state.logged_in:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login"):
                login(login_username, login_password)
                record_activity(login_username, "Login", "User logged in")
                
            st.subheader("Register")
            reg_username = st.text_input("New Username", key="reg_username")
            reg_password = st.text_input("New Password", type="password", key="reg_password")
            if st.button("Register"):
                register(reg_username, reg_password)
                record_activity(reg_username, "Register", "User registered")

        if st.session_state.logged_in:
            st.subheader("Welcome, " + st.session_state.username)
            movie_list = movies['title'].values
            selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)
            if st.button('Show Movie Details'):
                show_movie_details(selected_movie)
                record_activity(st.session_state.username, "Search", selected_movie)
            if st.button('Add to Watchlist'):
                add_to_watchlist(st.session_state.username, selected_movie)
            
            st.subheader('Rate a Movie')
            rating_movie = st.selectbox("Select a movie to rate", movie_list, key="rate_movie")
            rating_score = st.slider('Rate the movie', 1, 10, key="rate_score")
            if st.button('Submit Rating'):
                ratings = load_ratings()
                new_rating = pd.DataFrame([{
                    'username': st.session_state.username,
                    'movie_title': rating_movie,
                    'rating': rating_score
                }])
                ratings = pd.concat([ratings, new_rating], ignore_index=True)
                save_ratings(ratings)
                st.success(f"Rating for '{rating_movie}' submitted")
                record_activity(st.session_state.username, "Rate Movie", f"Rated '{rating_movie}' with {rating_score} points")

            st.subheader('Write a Review')
            review_movie = st.selectbox("Select a movie to review", movie_list, key="review_movie")
            review_text = st.text_area("Write your review here", key="review_text")
            if st.button('Submit Review'):
                reviews = load_reviews()
                new_review = pd.DataFrame([{
                    'username': st.session_state.username,
                    'movie_title': review_movie,
                    'review': review_text
                }])
                reviews = pd.concat([reviews, new_review], ignore_index=True)
                save_reviews(reviews)
                st.success(f"Review for '{review_movie}' submitted")
                record_activity(st.session_state.username, "Write Review", f"Reviewed '{review_movie}'")

            st.subheader('Your Watchlist')
            view_watchlist(st.session_state.username)

    elif page == "User History":
        set_background("static/background_history.jpg")

        if not st.session_state.logged_in:
            st.warning("Please log in to view your activity history.")
        else:
            activity = load_activity()
            user_activity = activity[(activity['username'] == st.session_state.username) & (activity['action'] == 'Search')]
            if not user_activity.empty:
                st.write("Movies you have searched for:")
                for _, row in user_activity.iterrows():
                    st.write(row['details'])
            else:
                st.write("No search activity recorded.")

    elif page == "Feedback":
        set_background("static/background_feedback.jpg")
        st.subheader("Feedback")
        feedback_text = st.text_area("Your feedback")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")
            record_activity(st.session_state.username, "Feedback", feedback_text)

    elif page == "Help":
        set_background("static/background_help.jpg")
        st.subheader("Help")
        st.write("""
        - Use the sidebar to navigate through different pages.
        - **Home**: Overview of the app.
        - **About**: Details about the app.
        - **Movie Recommender**: Get movie recommendations and rate movies.
        - **User History**: View your search and rating history.
        - **Feedback**: Provide your feedback about the app.
        - **Help**: Instructions on how to use the app.
        """)

if __name__ == "__main__":
    main()
