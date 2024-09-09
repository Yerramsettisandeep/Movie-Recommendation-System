Movie Recommendation System 🎬
Overview
The Movie Recommendation System is a web application that helps users discover new movies based on their interests. It uses machine learning algorithms to recommend movies based on similarity in genres, cast, crew, and other factors. Users can search for movies, view detailed information, and manage a personalized watchlist for movies they plan to watch.
"C:\Users\hi\Desktop\Projects\images\a0cc0c57-ac60-45cd-a343-3de0ac680497.jpg"
Features
Movie Recommendations: Based on genres, actors, directors, and movie metadata.
Watchlist: Users can save movies to watch later.
![Uploading 0c5e167d-99a2-4e4e-bf1c-d20236519603.jpg…]()
Search Functionality: Search for movies by title, genre, or actors.
![Uploading ad29d4f0-091b-444b-929b-b7312e86fffb.jpg…]()
Detailed Movie Info: Provides information like plot, release date, cast, and movie posters.
Rating System: Users can rate movies and provide feedback.

Tech Stack
Frontend: Streamlit for building the user interface.
Backend: Python with Pandas for data handling.
Machine Learning: Content-based filtering for movie recommendations.
Data: Movie metadata including titles, genres, cast, crew, and keywords.
Installation
Prerequisites
Python 3.x
Required Python packages:
pandas
streamlit
numpy
sklearn
requests

Navigate to the project directory:
cd Movie_Recommendation_System
Install the required packages:

pip install -r requirements.txt
Run the application:

streamlit run app.py
Usage
Open the app in your browser using the provided Streamlit link.
Search for a movie by title or browse recommendations based on selected genres.
Add movies to your personal watchlist or rate them.
View detailed information about each recommended movie.
Watchlist Feature
The Watchlist feature allows users to create and manage a personalized list of movies they plan to watch. Movies can be added to the watchlist with a single click and removed when no longer needed.
![5e340854-5625-4558-bc84-b5a8a3b72897](https://github.com/user-attachments/assets/a310ea9a-4d1d-4879-a3de-44432e7164e4)
login page and registration page:
![7638df42-1570-49bc-876f-48b43a9078e1](https://github.com/user-attachments/assets/b23cd191-6ac5-4c28-ab3a-00da402dff09)

Movie Recommendations
The system recommends movies based on:

Genres: Movies similar to the user's favorite genres.
Cast & Crew: Movies featuring similar actors or directors.
Movie Metadata: Plot descriptions and keywords are used to find similar content.
Data
This project uses movie data from TMDb. The data includes:
credits
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_credits.csv
movies
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv
install this 2 datasets.
Movie titles
Genres
Overviews
Cast and crew details
Keywords and other metadata
Future Enhancements
User authentication and personalized profiles.
Collaborative filtering for recommendations based on user ratings.
Improved recommendation accuracy using more advanced algorithms.
Contributing
Contributions are welcome! Please follow the steps below to contribute:
![8e57d32d-56e1-4703-a674-85c44ecf7594](https://github.com/user-attachments/assets/0c4205a6-40ce-4cde-add3-9c8c49787ccb)

License
This project is licensed under the MIT License. See the LICENSE file for more details.
