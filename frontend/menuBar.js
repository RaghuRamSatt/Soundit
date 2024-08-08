export default {
    data() {
        return {
            loginModal: false,
            loggedIn: false,
            signUpModal:false,
            searchModal:false,
            query:'',
            queryType:'',
            pass: '',
            email: '',
            dob:new Date(),
            searchArtists: [],
            searchAlbums: [],
            searchTracks: [],
            searchPlaylists: [],
            searchGenres: [],
            topArtists: [],
            topTracks:[],
            topPlaylists:[],
            topAlbums:[],
            searchUsers:[],
            topUsers:[],
            plans:[],
            showUsers:false,
            showArtists: false,
            showAlbums: false,
            showTracks: false,
            showPlaylists: false,
            showGenres: false,
            showPlans: false,
            newPlaylistModal: false,
            error:false,
            errorString: "",
            information:false,
            informationString: "",
            userManagement: false,
            playlistManagement: false,
            profileImg: "",
            showProfileImage: false,
            paymentMethod: "",
            viewListeningHistoryModal: false,
            historyTracks: [],
            playlistName: '',
            playlistImage: "",
            createdMode :false,
            currentPlaylist: ''
        }
    },
    created() {
        console.log("Menu bar built!");
    },
    methods:
    {
        async login() {
            const data = {username : this.username, password: this.pass}
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
            }


            let response = await fetch("http://127.0.0.1:5000/login", req);
            if (response.ok) {
                this.clean();
                let body = await response.json();
                this.loginModal = false;
                this.loggedIn = true;
                this.userRole = body;
                this.userLoggedIn();
            }  else {
                this.error = true;
                this.errorString = "Invalid username or password!";
            }
        },
        async accountManagement() {
            if(this.accountManagement) {
                this.userManagement = !this.userManagement;
                return;
            }
            await this.userLoggedIn();
            this.userManagement = true;
        },
        async userLoggedIn() {
            let response = await fetch(`http://127.0.0.1:5000/profile/${this.username}`);
            if (response.ok) {
                let body = await response.json();
                this.email = body.email;
                this.profileImg = body.profile_image;
                this.username = body.username;
                this.dob = body.date_of_birth;
                if(this.profileImg != "") { 
                    this.showProfileImage = true;
                }

                this.getRecommended();
            }
        },
        async getRecommended() {
            let response = await fetch(`http://127.0.0.1:5000/recommendations/${this.username}`);
            if(response.ok) {
                let body = await response.json();
                this.clean();
                this.searchTracks = [];
                body.recommendations.forEach((t) => {
                    this.searchTracks.push({
                        "track_id" : t.track_id,
                        "name" : t.track_name,
                        "file_path": t.file_path,
                        "duration": t.duration,
                    })
                });
                this.showTracks = true;
            }
        },
        async updateProfile() {
            if(this.password == "" ) {
                this.error = true;
                this.errorString = "Password is required to update user information!";
            }
            const data = {
                username : this.username, 
                password: this.password, 
                email: this.email, 
                date_of_birth: this.date_of_birth,
                profile_image: this.profileImg
            }
            const req = 
            {method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
            }
            let response = await fetch(`http://127.0.0.1:5000/profile/${this.username}`, req);
            print(response);
        },
        logout() {
            this.clean();
            this.loggedIn = false;
            this.profileImg = ''
            this.showProfileImage = false;
            this.username = ''
            this.pass = ''
            this.email = ''
            this.dob = new Date();
        },
        async signup() {
            const data = {username : this.username, password: this.pass, email: this.email, date_of_birth:this.dob}
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)}
            let response = await fetch("http://127.0.0.1:5000/register", req);

            if(response.ok) {
                this.login();
            } else {
                this.error = true;
                this.errorString = "Error while logging in!"
            }
        },
        home() {
            this.clean();
            this.query = '';
            this.error = false;
            this.errorString = '';
            this.information = false;
            this.informationString = ''
            if(this.loggedIn) {
                this.getRecommended();
            }
        },
        async search() {
            this.clean();
            let response = await fetch(`http://127.0.0.1:5000/search?term=${this.query}`);
            if(response.ok) {
                // display results
                let body = await response.json();
                
                this.searchAlbums = body.detailed_albums;
                this.searchArtists = body.detailed_artists;
                this.searchTracks = body.detailed_tracks;
                this.searchPlaylists = body.detailed_playlists;
                this.searchGenres = body.detailed_genres;
                this.searchUsers = body.detailed_users;
                
                
                this.topAlbums = body.top_albums;
                this.topArtists = body.top_artists;
                this.topTracks = body.top_tracks;
                this.topPlaylists = body.top_playlists;
                this.topGenres = body.top_genres;
                this.topUsers = body.top_users;

                this.showTracks = this.searchTracks.length > 0;
                this.showAlbums = this.searchAlbums.length > 0;
                this.showArtists = this.searchArtists.length > 0;
                this.showPlaylists = this.searchPlaylists.length > 0;
                this.showGenres = this.searchGenres.length > 0;
                this.showUsers = this.searchUsers.length > 0;
            } else {
                this.error = true;
                this.errorString = "Error while searching!";
            }
            
        },
        async viewPlaylist(id) {
            let response = await fetch(`http://127.0.0.1:5000/playlist?playlist_id=${id}`);
            if(response.ok) {
                let body = await response.json();
                if(body.tracks.length > 0) {
                    this.clean();
                    this.searchTracks = body.tracks;
                    this.showTracks = true;;
                }
            }
        }, 
        async deletePlaylist(id) {
            const data = {
                "creator_username" : this.username,
                "playlist_id" : id
            };
            const req = 
            {method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)};
            
            let response = await fetch("http://127.0.0.1:5000/playlist/delete", req);

            if(response.ok) {
                this.information = true;
                this.informationString = "Successfully deleted!";
            } else {
                this.error = true;
                this.errorString = "Error while deleting playlist!";
            }
        },
        async getArtist(name) {
            let response = await fetch(`http://127.0.0.1:5000/artist?name=${name}`);
            if(response.ok) {
                let body = await response.json();
                if(body.albums.length == 0 && body.tracks.length == 0) {
                    this.errorString = "No values returned!";
                    this.error = true;
                    return;
                }
                this.searchAlbums = [];
                body.albums.forEach((a) => {
                    this.searchAlbums.push({
                        "album_id": a.album_id, 
                        "name" : a.album_name, 
                        "artist_name": name, 
                        "image": a.album_image}
                    );
                });

                this.searchTracks = [];
                body.tracks.forEach((t) => {
                    this.searchTracks.push({
                        "track_id" : t.track_id,
                        "album_id" : t.album_id,
                        "duration" : t.duration,
                        "file_path" : t.file_path,
                        "name" : t.track_name,
                    })
                });
                this.clean();
                this.showAlbums = true;
                this.showTracks = true;
            }        
        },
        async getAlbum(id) {
            let response = await fetch(`http://127.0.0.1:5000/album?album_id=${id}`);
            if(response.ok) {
                let body = await response.json();
                this.clean();
                this.searchTracks = body.tracks;
                this.showTracks = true;
            }
        },
        async listen(id) {
            if(this.username === "") {
                this.error = true;
                this.errorString = "You must be logged in to utilize this functionality!";
                return;
            }
            let response = await fetch(`http://127.0.0.1:5000/track?track_id=${id}`);
            if(response.ok) {
                let body = await response.json();
                if(body[0].file_path !== undefined) {
                    let status = await this.notifyListen(id, this.username);
                    if(status) {
                        window.open(body[0].file_path).focus();
                    } else {
                        this.error = true;
                        this.errorString = "Error during playback!";
                    }
                } else { 
                    this.error = true;
                    this.errorString = "Cannot play this track at this time!";
                }
            }
        },
        async notifyListen(id, user) {
            const data = {
                "username" : user,
                "track_id" : id
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)}

            let response = await fetch("http://127.0.0.1:5000/record_listen", req)
            return response.ok;
        }, 
        async likeSong(id, name) {
            this.information = false;
            this.error = false;
            const data = {
                "username" : this.username,
                "track_id" : id
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)}

            let response = await fetch("http://127.0.0.1:5000/like_track", req);
            if(response.ok) {
                this.information = true;
                this.informationString = `Successfully liked song ${name}`;
            } else {
                this.error = true;
                this.errorString = `Error while liking song ${name}`;
            }

        },
        async followArtist(name) {
            this.information = false;
            this.error = false;
            const data = {
                "username" : this.username,
                "artist_name" : name
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)}

            let response = await fetch("http://127.0.0.1:5000/follow_artist", req);
            if(response.ok) {
                this.information = true;
                this.informationString = `Successfully followed ${name}!`
            } else {
                this.error = true;
                this.errorString = `Error while following ${name}!`;
            }
        },
        async followPlaylist(id, name) {
            this.information = false;
            this.error = false;
            const data = {
                "username" : this.username,
                "playlist_id" : id
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)}

            let response = await fetch("http://127.0.0.1:5000/follow_playlist", req);
            if(response.ok) {
                this.information = true;
                this.informationString = `Successfully followed ${name}!`
            } else {
                this.error = true;
                this.errorString = `Error while following ${name}!`;
            }
        },
        async getGenre(id) {
            let response = await fetch(`http://127.0.0.1:5000/genre?genre_id=${id}`);
            if(response.ok) {
                let body = await response.json();
            }   
        },
        async getPlans() {
            if(this.showPlans) {
                this.showPlans = !this.showPlans;
                return;
            }
            if(this.plans.length == 0) {
                let response = await fetch("http://127.0.0.1:5000/plans");
                if(response.ok) {
                    let body = await response.json();
                    this.plans = []
                    body.forEach((p) => {
                        if(p.duration != 99999) {
                            this.plans.push({               
                                "description": p.description,
                                "name" : p.name,
                                "price" : p.price,
                                "duration" : p.duration + " days"
                            });
                        } else {
                            this.plans.push({
                                "description": p.description,
                                "name" : p.name,
                                "price" : p.price,
                                "duration" : "N/A"
                            })
                        }
                    });
                    this.showPlans = true;
                }
            } else {
                this.showPlans = true;
            }    
        },
        async subscribe(planName) {
            if(this.username === '' || this.paymentMethod === "") {
                this.error = true;
                this.errorString = "Invalid username or payment method!";
            }
            const data = {
                "plan_name" : planName,
                "username" : this.username
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)};

            let response = await fetch(`http://127.0.0.1:5000/subscribe`, req);
            if(response.ok) {
                this.information = true;
                this.informationString = "Subscription successful!";
            }

            let index = this.plans.findIndex((plan) => {return plan.name == planName});
            const d1 = {
                "username" : this.username,
                "payment_method": this.paymentMethod,
                "amount": this.plans[index].price
            };
            const r1 = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(d1)};

            let payment = await fetch("http://127.0.0.1:5000/process_payment", r1)

            if(!payment.ok) {
                this.error = true;
                this.errorString = "Error while processing payment!";
                return;
            }
        },
        async cancelSub() {
            const data = {
                "username" : this.username
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)};

            let response = await fetch("http://127.0.0.1:5000/cancel_subscription", req);
            if(response.ok) {
                this.information = true;
                this.informationString = "Sucessfully unsubscribed!";
            } else {
                this.error = true;
                this.errorString = "Error while cancelling plan! You may be on the basic plan, which cannot be cancelled!";
            }
        },
        async viewListeningHistory() {
            let response = await fetch(`http://127.0.0.1:5000/listening_history/${this.username}`);
            if(response.ok) {
                this.clean();
                let body = await response.json();
                this.historyTracks = body.listening_history;
                this.viewListeningHistoryModal = true;
            }
        },
        async createPlaylist() {
            const data = {
                "name" : this.playlistName,
                "image" : this.playlistImage,
                "creator_username" : this.username
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)}

            let response = await fetch("http://127.0.0.1:5000/playlist/add", req);
            if(response.ok) {
                this.information = true;
                this.informationString = `Playlist ${this.playlistName} sucessfully created!`;
            } else {
                this.error = true;
                this.errorString = `Error while creating ${this.playlistName}!`
            }
        },
        async getYourPlaylists() {
            if(this.showPlaylists) {
                this.showPlaylists = false;
                return;
            }
            let response = await fetch(`http://127.0.0.1:5000/playlist/creator?creator_username=${this.username}`);
            if(response.ok) {
                let body = await response.json();
                if(body.playlists.length > 0) {
                    this.searchPlaylists = body.playlists;
                    this.showPlaylists = this.searchPlaylists.length > 0;
                    this.createdMode = true;
                }
            } else {
                this.error = true;
                this.errorString = "Error while fetching playlists. Are you sure that this user has playlists?"
            }

        },
        async addToPlaylist(trackId) {
            if(this.currentPlaylist == '') {
                this.error = true;
                this.errorString = "No currently selected playlist!";
            }
            const data = {
                "playlist_id" : this.currentPlaylist,
                "track_id" : trackId,
                "creator_username" : this.username
            };
            const req = 
            {method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)}
            let response = await fetch("http://127.0.0.1:5000/playlist/add_track", req);
            if(response.ok) {
                this.information = true;
                this.informationString = "Successfully added to playlist!"
            } else {
                this.error = true;
                this.errorString = "Error while adding to this playlist"
            }
        },
        prettyTime(duration) {
            let mins = Math.round(duration / 60000);
            let secs = Math.round((duration /  1000)) % 60;
            if(secs < 10) {
                secs = "0" + secs;
            }

            if (isNaN(mins) || isNaN(secs)) {
                return "0:00";
            } else {
                return `${mins}:${secs}`
            }
        },
        clean() {
            this.error = false;
            this.showAlbums = false;
            this.showArtists = false;
            this.showPlaylists = false;
            this.showTracks = false;
            this.loginModal = false;
            this.searchModal = false;
            this.signUpModal = false;
            this.showGenres = false;
            this.showPlans = false;
            this.information = false;
            this.userManagement = false;
            this.createdMode = false;
            this.playlistManagement = false;
            this.showUsers = false;
            this.viewListeningHistoryModal = false;
            this.cleanSearch();
        },
        cleanSearch() {
            this.showAlbums = false;
            this.showArtists = false;
            this.showTracks = false;
            this.showGenres = false;
            this.showPlaylists = false;
            this.showUsers = false;
        }
    }, 
    template: 
    `
    <div class="menu">
        <button @click=home()>Home</button>
        <button @click="searchModal=!searchModal"> Search </button>
        <button v-if="loggedIn" @click="playlistManagement=!playlistManagement">Playlists</button>
        <button v-if="loggedIn" @click="getPlans()"> View Plans </button>

        <button v-if="loggedIn" @click="accountManagement()"> {{this.username}} </button>

        <button v-if="!loggedIn" @click="loginModal=!loginModal">Login</button>
        <button v-if="!loggedIn" @click="signUpModal=!signUpModal">Sign Up</button>

        <button v-if="loggedIn" @click="logout()"> Sign Out </button>

        <img v-if="showProfileImage" v-bind:src="profileImg" width="25" height="25"/> 
    </div>


    <p v-if="error" style="color: red"> {{errorString}}</p>
    <p v-if="information"> {{informationString}} </p>

    <div v-if="playlistManagement">
    <button @click="getYourPlaylists()"> View your playlists </button>
    <button @click="newPlaylistModal = !newPlaylistModal"> Create a new playlist </button>
    

        <div v-if="newPlaylistModal">
            <form @submit.prevent="createPlaylist()">
                <label> Playlist Name </label>
                <input v-model="playlistName"/>
                <label> Playlist Image (Optional) </label>
                <input v-model="playlistImage"/>
                <button type=submit> Create! </button>
            </form>
        </div>
    </div>

    <div v-if="loginModal" @close="loginModal=false">
        <form @submit.prevent="login()">
            <label>Username</label><br>
            <input v-model="username"/><br>
            <label>Password</label><br>
            <input v-model="pass" type="password"/><br>
            <label> Sign in! </label><br>
            <button type=submit>Submit</button>
        </form>
    </div>

    <div v-if="signUpModal" @close="signUpModal=false">
        <form @submit.prevent="signup()">
            <label>Email</label><br>
            <input v-model="email"/><br>
            <label>Username</label><br>
            <input v-model="username"/><br>
            <label>Password</label><br>
            <input v-model="pass" type="password"/><br>
            <label>Date of Birth </label><br>
            <input v-model="dob" type="date"/><br> 
            <label> Sign up! </label><br>
            <button type=submit>Submit</button>
        </form>
    </div>

    <div v-if="searchModal" @close="searchModal=false">
        <form @submit.prevent="search()">
            <label>Enter your search here:</label><br>
            <input type=text v-model="query"/><br>
            <button type=submit> Search </button>
        </form>
    </div>



        <div v-if="showPlans">
            <h3> Available Plans </h3>
            <h5>Enter payment method here</h5> 
            <input v-model="paymentMethod"/>
            <table>
                <tr> <th></th> <th>Plan Name</th> <th>Plan Descriptions</th><th>Cost</th> <th>Duration</th></tr>
                <tr v-for="result in plans">
                    <td><button @click="subscribe(result.name)" > Subscribe! </button> </td>
                    <td>{{result.name}}</td>
                    <td>{{result.description}}</td>
                    <td>{{result.price}}</td>
                    <td>{{result.duration}} </td>
                </tr>
            </table>
        </div>
        

        <div v-if="userManagement">
            <form @submit.prevent="updateProfile()">
                <label>Email</label><br>
                <input v-model="email"/><br>
                <label>Username</label><br>
                <input v-model="username"/><br>
                <label>Date of Birth </label><br>
                <input v-model="dob" type="date"/><br> 
                <label> Profile Image </label> <br>
                <input v-model="profileImg"/><br>
                <label>Password</label><br>
                <input v-model="pass" type="password"/><br>
                <label> Update information </label><br>
                <button type=submit>Submit</button>
            </form>
            <button @click="viewListeningHistory()"> View your listening history </button>
        </div>

        <div v-if="viewListeningHistoryModal">
            <table>
            <tr><th> Track Name </th> <th>Number of plays </th> <th> Last played on</th> </tr>
            <tr v-for="result in historyTracks">
                <td>{{result.name}}</td> <td>{{result.play_count}}</td>  <td> {{result.play_date}} </td>
            </tr>
            </table>
        </div>

        <div class="searchResults">
        <div v-if="showAlbums">
            <h3> Albums </h3>
            <table>
                <tr @click="getAlbum(result.album_id)" v-for="result in searchAlbums"> 
                <img v-bind:src="result.image" width="50" height="50"/> {{result.name}} by {{result.artist_name}}</tr>
            </table>
            <br>
        </div>
        
        <div v-if="showArtists">
            <h3> Artists </h3>
            <table>
                <tr @click="getArtist(result.name)" v-for="result in searchArtists"> 
                <td><button @click="followArtist(result.name)"> Follow Artist</button></td>
                <td> <img v-bind:src="result.image" width="50" height="50"/> </td> 
                <td>{{result.name}} </td>
                </tr>
            </table>
            <br>
        </div>

        <div v-if="showPlaylists">
            <h3> Playlists </h3>

            <table>
                <tr v-for="result in searchPlaylists">
                <td> <button v-if="createdMode" @click="deletePlaylist(result.playlist_id); showPlaylists=false"> Delete this playlist </button> </td>
                <td> <button v-if="createdMode" @click="currentPlaylist=result.playlist_id; showPlaylists=false; searchModal=true"> Add songs to this playlist </button></td>
                <td> <button @click="followPlaylist(result.playlist_id, result.name)">Follow Playlist</button> </td>
                <td> <button @click="viewPlaylist(result.playlist_id)"> View Playlist </button> </td>
                <td v-if="result.image != ''"><img v-bind:src="result.image" width="50" height="50"/></td>
                <td>{{result.name}} </td>
                <td> Created by {{result.creator_username}} </td>

                </tr>
            </table>
        </div>

        <div v-if="showTracks">
            <h3> Tracks </h3>
            <table>
                <tr v-for="result in searchTracks">
                    <td><button @click="listen(result.track_id)">Listen</button></td>
                    <td><button @click="likeSong(result.track_id, result.name)">Add to Liked Songs</button></td>
                    <td><button v-if= "currentPlaylist != ''" @click="addToPlaylist(result.track_id)">  Add this song to a playlist </button> </td>
                    <td>{{result.name}}</td>
                    <td>{{prettyTime(result.duration)}}</td>
                 </tr>
            </table>
        </div>

        <div v-if="showUsers">
            <h3> Users </h3>

            <table>
                <tr @click="console.log(result.username)" v-for="result in searchUsers">{{result.username}}</tr>
            </table>
        </div>
        <div v-if="showGenres">
            <h3> Genres </h3>
            <table>
                <tr @click="getGenre(result.genre_id)" v-for="result in searchGenres">
                    {{result.name}}
                </tr>
            </table>
        </div>
    </div>
    `
}