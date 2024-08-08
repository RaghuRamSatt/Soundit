# Soundit

## Introduction

Soundit is a sophisticated music streaming application designed to deliver an enriching and interactive experience to music enthusiasts. This application allows users to explore a vast collection of music, create and manage playlists, follow their favorite artists, and enjoy a personalized music experience based on their preferences and listening history.

## Features

- User authentication and profile management
- Music browsing and advanced search functionality
- Playlist creation and management
- Artist and playlist following
- Track liking and detailed listening history
- Subscription management with various plans
- Personalized recommendations based on user activity
- Admin panel for content management

## Technologies Used

- Backend: Python 3.10.8, Flask 2.25
- Frontend: Vue.js, Node.js v14.18.0, npm 9.4.0
- Database: MySQL 8.0
- Data Import: Spotify API
- Development Environment: Spyder IDE

## Prerequisites

- Python 3.10.8 or higher
- Node.js v14.18.0 or higher
- npm 9.4.0 or higher
- MySQL Workbench 8.0
- Spyder IDE (recommended for backend development)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RaghuRamSatt/soundit.git
cd soundit
```


### 2. Database Setup

1. Install MySQL Workbench 8.0 from [MySQL Downloads](https://dev.mysql.com/downloads/workbench/).
2. Open MySQL Workbench.
3. Import the "Soundit-dump-2" MySQL dump file to create the Soundit_test_2 schema.

### 3. Backend Setup

1. Install Python 3.10.8 from [Python Downloads](https://www.python.org/downloads/).
2. Create and activate a virtual environment:


```bash
python -m venv venv
source venv/bin/activate # On Windows use venv\Scripts\activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```


4. Update the database connection settings in `server/app.py`:

```python
connection = pymysql.connect(host='localhost',
user='your_username',
password='your_password',
db='soundit_test_2',
charset='utf8mb4',
cursorclass=pymysql.cursors.DictCursor)
```



### 4. Frontend Setup

1. Install Node.js v14.18.0 from [Node.js Downloads](https://nodejs.org/en/download/).
2. Navigate to the frontend directory:

```bash
cd frontend
```

3. Install frontend dependencies:

```bash
npm install
```


## Usage

### 1. Start the Backend Server

1. Navigate to the server directory:

```bash
cd server
```

2. Run the Flask application:

```bash
python app.py
```


The backend server should now be running on `http://localhost:5000`.

### 2. Start the Frontend Server

1. Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```


2. Start the frontend server:

```bash
npx serve
```


The frontend should now be accessible at `http://localhost:3000`.

### 3. Accessing Soundit

Open your web browser and go to `http://localhost:3000` to access the Soundit application.

## Importing Data

### Importing Artist Data

1. Navigate to the utils folder:

```bash
cd utils
```

2. Run the artist_data_import.py script:

```bash
python data_import.py
python genre_insert.py
```



### Getting Additional Spotify Data

1. Navigate to the getSpotifyData folder:

```bash
cd getSpotifyData
```


2. Open `generate_data.py` and fill in the `ID` and `SECRET` constant variables with your Spotify API credentials.
3. Edit the `artists.csv` file with Spotify Artist IDs you want to import.
4. Run the data generation script:

```bash
python generate_data.py
```


## Project Structure

- `server/`: Contains the Flask backend application
  - `app.py`: Main application file with API endpoints
- `frontend/`: Contains the Vue.js frontend application
  - `index.html`: Entry point for the frontend
  - `menuBar.js`: Main Vue component for the application
  - `admin.js`: Admin panel component
- `utils/`: Utility scripts for data import
- `getSpotifyData/`: Scripts for fetching data from Spotify API
- `README.md`: This file
- `requirements.txt`: Python dependencies

## API Documentation

The Soundit API provides the following main endpoints:

- `/register`: User registration
- `/login`: User authentication
- `/search`: Search for artists, albums, tracks, and playlists
- `/artist`: Get artist details
- `/album`: Get album details
- `/track`: Get track details
- `/playlist`: Manage playlists
- `/recommendations`: Get personalized recommendations

For a complete list of endpoints and their usage, refer to the comments in `server/app.py`.

## Contributing

I thank my two teammates (Nicholas Patel and Jinpeng Chen) for their help in this project.

## Data Usage and Spotify API

This project uses data obtained from the Spotify API for educational and demonstration purposes only. Please note the following important points:

1. **Data Source**: The music data used in this application is sourced from the Spotify API. We do not claim ownership of this data.

2. **Usage Restrictions**: The data obtained from Spotify should not be used for any commercial purposes. It is strictly for educational use within the context of this project.

3. **Spotify Developer Terms**: If you plan to run this application or use the data import scripts, you must comply with Spotify's Developer Terms of Service. Please review these terms at [Spotify Developer Terms](https://developer.spotify.com/terms).

4. **API Credentials**: To use the data import functionality, you will need to obtain your own Spotify API credentials. Do not share these credentials publicly.

5. **Data Limitations**: The data provided by this application may not be up-to-date or complete. For the most current and accurate information, please refer to the official Spotify platform.

6. **No Affiliation**: This project is not affiliated with, endorsed by, or sponsored by Spotify. It is an independent educational project.

7. **Respect Copyright**: Ensure that your use of this application and its data respects all applicable copyright laws and Spotify's intellectual property rights.

By using this application or its code, you agree to abide by these terms and any applicable laws and regulations regarding the use of third-party data and APIs.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Spotify API for providing music data
- Flask community for the excellent web framework
- Vue.js team for the frontend framework

## Contact

Raghu Ram Sattanapalle

Project Link: https://github.com/RaghuRamSatt/soundit