# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 11:09:00 2023

@author: raghu
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import sys
import re  # Add regex for email validation
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # For password hashing
import json  
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a random key for session management
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def create_db_connection():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='test',
                                     db='soundit_test_2',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Database: {e}", file=sys.stderr)
        return None

@app.route('/', methods=['GET'])
def home():
    return "Welcome to Soundit API! ~~~~~~"


# # 1. User Account Management

# # 1.1 Create Account (Create):

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    profile_image = data.get('profile_image', '')
    date_of_birth = data.get('date_of_birth')
    plan_name = data.get('plan_name', 'basic')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('RegisterUser', [username, email, password, profile_image, date_of_birth, plan_name])
            connection.commit()
        return jsonify({'success': 'User registered successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

        
@app.route('/register_admin', methods=['POST'])
def register_admin_user():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    profile_image = data.get('profile_image', '')
    date_of_birth = data.get('date_of_birth')
    secure_key = data.get('secure_key')  # Secure key for admin account creation

    # Check for the presence of the secure key
    if not secure_key:
        return jsonify({'error': 'Secure key is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            # Pass the secure key along with other details to the stored procedure
            cursor.callproc('RegisterAdminUser', [username, email, password, profile_image, date_of_birth, secure_key])
            connection.commit()
        return jsonify({'success': 'Admin user registered successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

        
# 1.2 Login (Read):
    
@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            # Prepare the parameters including placeholders for the output values
            params = [username, password, 0, '']
            cursor.callproc('UserLogin', params)
            
            # Fetch the output values
            cursor.execute('SELECT @_UserLogin_2, @_UserLogin_3')
            output = cursor.fetchone()
            login_success = output['@_UserLogin_2']
            user_role = output['@_UserLogin_3']


            if login_success:
                # session['username'] = username  # Store the username in the session
                # session['role'] = user_role     # Store the user's role
                return jsonify({'success': 'Logged in successfully', 'role': user_role}), 200
            else:
                return jsonify({'error': 'Invalid username or password'}), 401
            # if login_success:
            #     return jsonify({'success': 'Logged in successfully', 'role': user_role}), 200
            # else:
            #     # This else part will not be reached if a SQLSTATE '45000' error is raised in MySQL
            #     return jsonify({'error': 'Invalid username or password'}), 401
    except pymysql.MySQLError as e:
        # Custom error message handling from MySQL stored procedure
        return jsonify({'error': str(e.args[1])}), 400  # e.args[1] contains the custom error message
    finally:
        connection.close()


 # # 1.3 View/Edit Profile (Read/Update):       

 # View User Profile
@app.route('/profile/<username>', methods=['GET'])
def view_user_profile(username):
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            # Adding a placeholder for the OUT parameter
            cursor.execute("CALL ViewUserProfile(%s, @p_user_info);", (username,))
            cursor.execute("SELECT @p_user_info;")
            result = cursor.fetchone()

            if result and '@p_user_info' in result and result['@p_user_info']:
                return jsonify(json.loads(result['@p_user_info'])), 200
            else:
                return jsonify({'error': 'User not found'}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()




# Update User Profile
@app.route('/profile/<username>', methods=['PUT'])
def update_user_profile(username):
    requesting_user = request.headers.get('Username')
    user_role = request.headers.get('UserRole')

    data = request.json
    email = data.get('email', None)
    profile_image = data.get('profile_image', None)
    new_password = data.get('new_password', None)
    date_of_birth = data.get('date_of_birth', None)

    # Hash the new password if provided
    new_password_hash = generate_password_hash(new_password) if new_password else None

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('UpdateUserProfile', [requesting_user, username, email, profile_image, new_password_hash, date_of_birth])
            connection.commit()
            return jsonify({'success': 'Profile updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# # -------------------------------------------------------------

# # 2. Subscription and Payment Handling

# # View/Choose Subscription Plans (Read/Create):
    
@app.route('/plans', methods=['GET'])
def get_subscription_plans():
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            # Prepare a placeholder for the output parameter
            cursor.execute('CALL GetSubscriptionPlans(@p_plans)')
            cursor.execute('SELECT @p_plans AS p_plans')
            results = cursor.fetchall()
            if results and 'p_plans' in results[0]:
                return jsonify(json.loads(results[0]['p_plans'])), 200
            else:
                return jsonify({'error': 'No subscription plans found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/subscribe', methods=['POST'])
def subscribe_to_plan():
    data = request.json
    username = data.get('username')
    plan_name = data.get('plan_name')

    if not username or not plan_name:
        return jsonify({'error': 'Username and plan name are required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('SubscribeToPlan', [username, plan_name])
        connection.commit()
        return jsonify({'message': 'Subscription process initiated'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400  # e.args[1] contains the custom error message
    finally:
        connection.close()


@app.route('/cancel_subscription', methods=['POST'])
def cancel_subscription():
    data = request.json
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('CancelSubscription', [username])
        connection.commit()
        return jsonify({'message': 'Subscription cancellation process initiated'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400  # e.args[1] contains the custom error message
    finally:
        connection.close()


@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    username = data.get('username')
    payment_method = data.get('payment_method')
    amount = data.get('amount')

    if not all([username, payment_method]):
        return jsonify({'error': 'Username, payment method, and amount are required'}), 400
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
    try:
        with connection.cursor() as cursor:
            cursor.callproc('ProcessPayment', [username, payment_method, amount])
        connection.commit()
        return jsonify({'message': 'Payment processed successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400  # e.args[1] contains the custom error message
    finally:
        connection.close()

# # -------------------------------------------------------------

# # 3. Music Browsing and Management

# # Search (Read):
    
@app.route('/search', methods=['GET'])
def comprehensive_search():
    search_term = request.args.get('term')

    if not search_term:
        return jsonify({'error': 'Search term is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc('ComprehensiveSearch', [search_term])
            
            # Initialize the dictionary to store results
            search_results = {
                'top_artists': [],
                'top_albums': [],
                'top_tracks': [],
                'top_playlists': [],
                'top_genres': [],
                'top_users': [],
                'detailed_artists': [],
                'detailed_albums': [],
                'detailed_tracks': [],
                'detailed_playlists': [],
                'detailed_genres': [],
                'detailed_users': []
            }

            # Fetch top artists
            if cursor.rowcount > 0:
                search_results['top_artists'] = cursor.fetchall()

            # Fetch top albums
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['top_albums'] = cursor.fetchall()

            # Fetch top tracks
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['top_tracks'] = cursor.fetchall()

            # Fetch top playlists
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['top_playlists'] = cursor.fetchall()

            # Fetch top genres
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['top_genres'] = cursor.fetchall()

            # Fetch top users
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['top_users'] = cursor.fetchall()

            # Fetch detailed artists results
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['detailed_artists'] = cursor.fetchall()

            # Fetch detailed albums results
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['detailed_albums'] = cursor.fetchall()

            # Fetch detailed tracks results
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['detailed_tracks'] = cursor.fetchall()

            # Fetch detailed playlists results
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['detailed_playlists'] = cursor.fetchall()

            # Fetch detailed genres results
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['detailed_genres'] = cursor.fetchall()

            # Fetch detailed users results
            if cursor.nextset() and cursor.rowcount > 0:
                search_results['detailed_users'] = cursor.fetchall()

            return jsonify(search_results), 200

    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/artist', methods=['GET'])
def search_artist_by_name():
    artist_name = request.args.get('name')

    # Input validation
    if not artist_name or artist_name.strip() == '':
        return jsonify({'error': 'Artist name is required and cannot be blank'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc('SearchArtistByName', [artist_name])

            albums = cursor.fetchall()

            # Check if there is a next result set for tracks
            tracks = []
            if cursor.nextset():
                tracks = cursor.fetchall()

            if not albums and not tracks:
                return jsonify({'error': f'No albums or tracks found for artist: {artist_name}'}), 404

            response = {
                'artist_name': artist_name,
                'albums': albums,
                'tracks': tracks
            }
            return jsonify(response), 200

    except pymysql.MySQLError as e:
        return jsonify({'error': f'SQL error: {str(e)}'}), 500
    finally:
        connection.close()


@app.route('/user', methods=['GET'])
def search_user_by_username():
    username = request.args.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('SearchUserByUsername', [username])
            results = cursor.fetchall()
            if results:
                return jsonify(results), 200
            else:
                return jsonify({'error': 'User not found'}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/genre', methods=['GET'])
def search_genre_by_id():
    genre_id = request.args.get('genre_id', type=int)

    if genre_id is None:
        return jsonify({'error': 'Genre ID is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc('SearchGenreById', [genre_id])
            
            # Fetch genre details
            genre_results = cursor.fetchall()
            if not genre_results:
                return jsonify({'error': 'Genre not found'}), 404

            # Fetch tracks associated with the genre
            cursor.nextset()  # Move to the next result set
            track_results = cursor.fetchall()

            return jsonify({'genre': genre_results, 'tracks': track_results}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/album', methods=['GET'])
def search_album_by_id():
    album_id = request.args.get('album_id', type=int)

    if album_id is None:
        return jsonify({'error': 'Album ID is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc('SearchAlbumById', [album_id])
            album_results = cursor.fetchall()

            # Fetch the next result set for tracks
            if cursor.nextset():
                track_results = cursor.fetchall()
                results = {'album': album_results, 'tracks': track_results}
            else:
                results = {'album': album_results, 'tracks': []}

            if album_results:
                return jsonify(results), 200
            else:
                return jsonify({'error': 'Album not found'}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/track', methods=['GET'])
def search_track_by_id():
    track_id = request.args.get('track_id', type=int)

    if track_id is None:
        return jsonify({'error': 'Track ID is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('SearchTrackById', [track_id])
            results = cursor.fetchall()
            if results:
                return jsonify(results), 200
            else:
                return jsonify({'error': 'Track not found'}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/playlist', methods=['GET'])
def search_playlist_by_id():
    playlist_id = request.args.get('playlist_id', type=int)

    if playlist_id is None:
        return jsonify({'error': 'Playlist ID is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.callproc('SearchPlaylistById', [playlist_id])
            playlist_results = cursor.fetchall()

            # Fetch the next result set for tracks
            if cursor.nextset():
                track_results = cursor.fetchall()
                results = {'playlist': playlist_results, 'tracks': track_results}
            else:
                results = {'playlist': playlist_results, 'tracks': []}

            if playlist_results:
                return jsonify(results), 200
            else:
                return jsonify({'error': 'Playlist not found'}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


# CRUD Artist:
#  This endpoint is restricted to admin users. It allows adding a new artist to the database.

@app.route('/admin/artist', methods=['POST'])
def add_artist():
    data = request.json
    name = data.get('name')
    image = data.get('image')
    admin_role = data.get('admin_role') 
    admin_token = data.get('admin_token')

    if admin_role != 'admin' or not admin_token or admin_token != 'adminCRUD':
        return jsonify({'error': 'Unauthorized access'}), 403

    if not name or not image:
        return jsonify({'error': 'Missing data'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('AddArtist', [name, image, admin_role, admin_token])
            connection.commit()
            return jsonify({'success': 'Artist added successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/admin/artist/update', methods=['PUT'])
def update_artist():
    data = request.json
    artist_name = data.get('name')
    new_image = data.get('image')
    admin_role = data.get('admin_role') 
    admin_token = data.get('admin_token')

    if admin_role != 'admin' or admin_token != 'adminCRUD':
        return jsonify({'error': 'Unauthorized access'}), 403

    if not artist_name or not new_image:
        return jsonify({'error': 'Missing data'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('UpdateArtist', [artist_name, new_image, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': f'Artist {artist_name} updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@app.route('/admin/artist/delete', methods=['DELETE'])
def delete_artist():
    data = request.json

    artist_name = data.get('name')  
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    if admin_role != 'admin' or admin_token != 'adminCRUD':
        return jsonify({'error': 'Unauthorized access'}), 403

    if not artist_name:
        return jsonify({'error': 'Artist name is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('DeleteArtist', [artist_name, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': f'Artist {artist_name} deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# CRUD Genre:
    
@app.route('/admin/genre', methods=['POST'])
def add_genre():
    data = request.json
    genre_name = data.get('genre_name')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    if admin_role != 'admin' or admin_token != 'adminCRUD':
        return jsonify({'error': 'Unauthorized access'}), 403

    if not genre_name:
        return jsonify({'error': 'Genre name is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('AddGenre', [genre_name, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': f'Genre {genre_name} added successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
    
    
@app.route('/admin/genre/update', methods=['PUT'])
def update_genre():
    data = request.json
    old_name = data.get('genre_name')
    new_name = data.get('new_genre')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')


    if admin_role != 'admin' or admin_token != 'adminCRUD':
        return jsonify({'error': 'Unauthorized access'}), 403

    if not old_name or not new_name:
        return jsonify({'error': 'Both old and new genre names are required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('UpdateGenre', [old_name, new_name, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': f'Genre updated from {old_name} to {new_name}'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()


@app.route('/admin/genre/delete', methods=['DELETE'])
def delete_genre():
    data = request.json
    genre_name = data.get('genre_name')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    if admin_role != 'admin' or admin_token != 'adminCRUD':
        return jsonify({'error': 'Unauthorized access'}), 403

    if not genre_name:
        return jsonify({'error': 'Genre name is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('DeleteGenre', [genre_name, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': f'Genre {genre_name} deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# CRUD Album:

@app.route('/admin/album', methods=['POST'])
def add_album():
    data = request.json
    name = data.get('name')
    release_date = data.get('release_date')  # Expected format: 'YYYY-MM-DD'
    image = data.get('image')
    artist_name = data.get('artist_name')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('AddAlbum', [name, release_date, image, artist_name, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': f'Album {name} added successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()

@app.route('/admin/album/update', methods=['PUT'])
def update_album():
    data = request.json
    album_id = data.get('album_id')
    new_name = data.get('name')
    new_release_date = data.get('release_date')
    new_image = data.get('image')
    new_artist_name = data.get('artist_name')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('UpdateAlbum', [album_id, new_name, new_release_date, new_image, new_artist_name, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': 'Album updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()

@app.route('/admin/album/delete', methods=['DELETE'])
def delete_album():
    data = request.json
    album_id = data.get('album_id')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('DeleteAlbum', [album_id, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': 'Album deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()


# CRUD Track:

@app.route('/admin/track', methods=['POST'])
def add_track():
    data = request.json
    name = data.get('name')
    duration = data.get('duration')
    file_path = data.get('file_path')
    album_id = data.get('album_id')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('AddTrack', [name, duration, file_path, album_id, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': f'Track {name} added successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()

        
@app.route('/admin/track/update', methods=['PUT'])
def update_track():
    data = request.json
    track_id = data.get('track_id')
    new_name = data.get('name')
    new_duration = data.get('duration')
    new_file_path = data.get('file_path')
    new_album_id = data.get('album_id')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('UpdateTrack', [track_id, new_name, new_duration, new_file_path, new_album_id, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': 'Track updated successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()


@app.route('/admin/track/delete', methods=['DELETE'])
def delete_track():
    data = request.json
    track_id = data.get('track_id')
    admin_role = data.get('admin_role')
    admin_token = data.get('admin_token')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('DeleteTrack', [track_id, admin_role, admin_token])
            connection.commit()
        return jsonify({'success': 'Track deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()
   
 
# CRUD Playlist:
    
@app.route('/playlist/add', methods=['POST'])
def add_playlist():
    data = request.json
    name = data.get('name')
    image = data.get('image', '')
    creator_username = data.get('creator_username')

    if not creator_username:
        return jsonify({'error': 'Creator username is required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('AddPlaylist', [name, image, creator_username])
            connection.commit()
        return jsonify({'success': f'Playlist {name} created successfully'}), 201
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400  # e.args[1] contains the custom error message
    finally:
        connection.close()


@app.route('/playlist/delete', methods=['DELETE'])
def delete_playlist():
    data = request.json
    playlist_id = data.get('playlist_id')
    creator_username = data.get('creator_username')  # Username of the creator of the playlist

    if playlist_id is None or creator_username is None:
        return jsonify({'error': 'Playlist ID and creator username are required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('DeletePlaylist', [playlist_id, creator_username])
            connection.commit()
        return jsonify({'success': f'Playlist with ID {playlist_id} deleted successfully'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400  # e.args[1] contains the custom error message
    finally:
        connection.close()


@app.route('/playlist/add_track', methods=['POST'])
def add_track_to_playlist():
    data = request.json
    playlist_id = data.get('playlist_id')
    track_id = data.get('track_id')
    creator_username = data.get('creator_username')  # Username of the creator of the playlist

    # Validation of input data
    if playlist_id is None or track_id is None or not creator_username:
        return jsonify({'error': 'Playlist ID, track ID, and creator username are required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            # Call the stored procedure with the provided parameters
            cursor.callproc('AddTrackToPlaylistByCreator', [playlist_id, track_id, creator_username])
            connection.commit()
        return jsonify({'success': 'Track added to playlist successfully'}), 201
    except pymysql.MySQLError as e:
        # e.args[1] contains the custom error message from the stored procedure
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()

@app.route('/playlist/remove_track', methods=['POST'])
def remove_track_from_playlist():
    data = request.json
    playlist_id = data.get('playlist_id')
    track_id = data.get('track_id')
    creator_username = data.get('creator_username')  # Username of the creator of the playlist

    # Validation of input data
    if playlist_id is None or track_id is None or not creator_username:
        return jsonify({'error': 'Playlist ID, track ID, and creator username are required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            # Call the stored procedure with the provided parameters
            cursor.callproc('RemoveTrackFromPlaylistByCreator', [playlist_id, track_id, creator_username])
            connection.commit()
        return jsonify({'success': 'Track removed from playlist successfully'}), 200
    except pymysql.MySQLError as e:
        # e.args[1] contains the custom error message from the stored procedure
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()


# To track user listening of tracks

@app.route('/record_listen', methods=['POST'])
def record_listen():
    data = request.json
    username = data.get('username')
    track_id = data.get('track_id')

    if not username or not track_id:
        return jsonify({'error': 'Username and track ID are required'}), 400

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('RecordUserListen', [username, track_id])
            connection.commit()
            return jsonify({'success': 'Track listen recorded successfully'}), 200
    except pymysql.MySQLError as e:
        connection.rollback()  # Rollback in case of error
        return jsonify({'error': 'An error occurred while recording the track listen'}), 500
    finally:
        connection.close()


# Endpoint for following artist

@app.route('/follow_artist', methods=['POST'])
def follow_artist():
    data = request.json
    username = data.get('username')
    artist_name = data.get('artist_name')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('FollowArtist', [username, artist_name])
            connection.commit()
        return jsonify({'success': f'Following artist {artist_name}'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()

# Endpoint for following playlists

@app.route('/follow_playlist', methods=['POST'])
def follow_playlist():
    data = request.json
    username = data.get('username')
    playlist_id = data.get('playlist_id')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('FollowPlaylist', [username, playlist_id])
            connection.commit()
        return jsonify({'success': f'Following playlist {playlist_id}'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()


# User likes a track 

@app.route('/like_track', methods=['POST'])
def like_track():
    data = request.json
    username = data.get('username')
    track_id = data.get('track_id')

    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('LikeTrack', [username, track_id])
            connection.commit()
        return jsonify({'success': f'Liked track {track_id}'}), 200
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e.args[1])}), 400
    finally:
        connection.close()

# get history for user listening to tracks

@app.route('/listening_history/<username>', methods=['GET'])
def get_listening_history(username):
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        with connection.cursor() as cursor:
            cursor.callproc('GetUserListeningHistory', [username])
            results = cursor.fetchall()
            if results:
                return jsonify({'listening_history': results}), 200
            else:
                return jsonify({'message': 'No listening history found'}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# Get 20 recommendations for users

# Get 20 recommendations for users
 
 
@app.route('/recommendations/<username>', methods=['GET'])
def get_user_recommendations(username):
    # Establish a connection to the database
    connection = create_db_connection()
    if connection is None:
        return jsonify({'error': 'Database connection failed'}), 500
 
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Call the stored procedure to get user recommendations
            cursor.callproc('GetUserRecommendations', [username])
            recommendations = cursor.fetchall()
            # Check if recommendations are found
            if recommendations:
                return jsonify({'recommendations': recommendations}), 200
            else:
                return jsonify({'message': 'No recommendations found'}), 404
    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close() # Close the database connection


@app.route('/playlist/creator', methods=['GET'])

def search_playlists_by_creator():

    creator_username = request.args.get('creator_username')
 
    if not creator_username:

        return jsonify({'error': 'Creator username is required'}), 400
 
    connection = create_db_connection()

    if connection is None:

        return jsonify({'error': 'Database connection failed'}), 500
 
    try:

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            cursor.callproc('SearchPlaylistsByCreatorUsername', [creator_username])

            results = cursor.fetchall()

            if results:

                return jsonify({'playlists': results}), 200

            else:

                return jsonify({'error': 'No playlists found for the given creator'}), 404

    except pymysql.MySQLError as e:
        return jsonify({'error': str(e)}), 500

    finally:

        connection.close()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

