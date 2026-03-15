# Billy's Movie List App 🎬
**CS50x Final Project – December 2025**

#### Video Demo:  https://youtu.be/rZJoRj4AqiA?si=rJ0q9ZvtOolING1-

## Overview  🌐
Billy's Movie List App is a full-featured web application that brings my brother's lifelong curated collection of essential films to life. Over three decades, Billy has carefully selected more than 1,300 movies — spanning silent classics to modern masterpieces — based on artistic merit, historical importance, and cinematic excellence. This app transforms that personal canon into an interactive, community-driven platform for discovering great cinema.

Unlike algorithm-heavy streaming services, this app celebrates human curation. Every film earns its place through thoughtful selection, not popularity contests. Users can explore the collection, search by genre, decade, or director, build personal watchlists, rate films, view their own top-rated discoveries, and see real-time activity from other users exploring the list.
Features

## Key Features  ✨
### Curated Collection
Over 1,300 hand-picked films seeded from The Movie Database (TMDB) API, complete with high-quality posters, release years, genres, and director information.

### Advanced Search
Filter the collection by:
- Genre (Drama, Comedy, Horror, Documentary, etc.)
- Decade (Pre-1930 through 2020s)
- Director (e.g., "Fritz Lang", "Akira Kurosawa", "John Ford")
- Searches can be combined for precise discovery (e.g., "1940s Drama" or "Science Fiction 1950s").

### Personal Watchlist
Registered users can:
- Add any movie to their watchlist
- Rate films on a 1–10 scale
- View all rated and unrated movies in organized sections
- See a dedicated "My Top Rated" showcase with gold borders for highest-rated films

### Community Activity Feed
Real-time "/recent-activity" page showing what other users are adding, with usernames, movie posters, and timestamps — creating a sense of shared discovery.

### Responsive Design
Fully mobile-friendly with adaptive card grids, smaller posters on phones, and touch-optimized navigation.
### Cinematic / Heavy Metal Theme
Dark background with vibrant purple primary accents and white text, inspired by classic movie theaters and modern streaming interfaces. Custom, Black Sabbath inspired logo to honor Billy's other passion: heavy metal.

## Technical Implementation 🛠️
Built with the Flask web framework and SQLite database using the CS50 SQL library.
Key technologies:

- Flask + Flask-Session for user authentication and sessions
- SQLite for persistent storage of users, watchlist, and timestamps
- TMDB API for movie data, posters, genres, and directors
- Bootstrap 5 for responsive layout
- Custom CSS with Bebas Neue and Inter fonts for elegant typography
- Parameterized SQL queries throughout for security

Database schema includes:

- users — authentication
- movies — curated films with title, year, poster, genres, director
- watchlist — user-movie relationships with rating and timestamp

## Development Highlights 📚
This project represents the culmination of CS50x learning:

- Secure user authentication with password hashing
- Complex SQL joins for watchlist, top-rated, and activity feed
- External API integration with TMDB (search, details, credits endpoints)
- Responsive design principles
- Error handling and user feedback via flash messages
- Iterative development with extensive debugging of API and database issues

## Future Ideas 🔮

- User profiles with public watchlists
- Discussion threads per film
- Streaming availability integration
- Recommendation engine based on community ratings
- Mobile app version

## Acknowledgments 🙏
Special thanks to my brother Billy for sharing his extraordinary movie list — the heart of this app.

Thank you to the CS50x faculty and staff for the knowledge and inspiration.

Built with 💜 in Chicago.
