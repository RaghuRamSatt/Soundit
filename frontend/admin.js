export default {
    data() {
        return {
            signedIn : false,
            username: '',
            password : '',
            regKey : '',
            role : '',
            error: false,
            errorString: "",
            information : false,
            informationString : '',
            adminModal: false,
            artistModal: false,
            albumModal:false,
            trackModal:false,
            genreModal:false,

            newAdminUsername:'',
            newAdminPass:'',
            newAdminDOB:'',
            newAdminEmail:'',

            artistMode: '',
            artistName: '',
            artistImage: '',

            oldGenreName: '',
            newGenreName: '',
            genreMode: '',

            albumMode:'',
            albumId:'',
            albumName:'',
            albumRelease:'',
            albumImage:'',

            trackMode:'',
            trackId:'',
            trackName:'',
            trackDuration:'',
            trackPath:'',

            token: 'adminCRUD'
        }      
    },
    methods: 
    {
        async loginAdmin() {
            if(this.username == '' || this.password == '' || this.regKey == '') {
                this.error = true;
                this.errorString = "Invalid login information!"
            } 
            let data = {
                'username' : this.username,
                'password' : this.password
            }
            const req = this.buildRequest("POST", data);
            let response = await fetch("http://127.0.0.1:5000/login", req);
            
            if(response.ok) {
                let body = await response.json();
                this.signedIn = true;
                this.role = body.role;
            }
        },
        async registerAdmin() {
            let data = {
                "username" : this.newAdminUsername,
                "email" : this.newAdminEmail,
                "password" : this.newAdminPass,
                "date_of_birth" : this.newAdminDOB,
                "secure_key" : this.regKey
            };
            const req = this.buildRequest("POST", data);

            let response = await fetch("http://127.0.0.1:5000/register_admin", req);
            
            if(response.ok) {
                this.information = true;
                this.informationString = "Successfully created new admin account!";
            } else {
                this.error = true;
                this.errorString = "Error while creating admin account!";
            }

        },

        async createNewArtist() {
            if(this.artistMode != "create") {
                this.artistMode = "create";
                this.artistModal = true;
            } else {
                this.artistMode = "";
                this.artistModal = false;
            }
        },
        async createNewGenre() {
            if(this.genreMode != "create") {
                this.genreMode = "create";
                this.genreModal = true;
            } else {
                this.genreMode = "";
                this.genreModal = false;
            }
        },
        async createNewAlbum() {
            if(this.albumMode != "create") {
                this.albumMode = "create";
                this.albumModal = true;
            } else {
                this.albumMode = "";
                this.albumModal = false;
            }
        },
        async createNewTrack() {
            if(this.trackMode != "create") {
                this.trackMode = "create";
                this.trackModal = true;
            } else {
                this.trackMode = "";
                this.trackModal = false;
            }
        },
        async updateArtist() {
            if(this.artistMode != "update") {
                this.artistMode = "update";
                this.artistModal = true;
            } else {
                this.artistMode = "";
                this.artistModal = false;
            }

        },
        async updateGenre() {
            if(this.genreMode != "update") {
                this.genreMode = "update";
                this.genreModal = true;
            } else {
                this.genreMode = "";
                this.genreModal = false;
            }
        },
        async updateAlbum() {
            if(this.albumMode != "update") {
                this.albumMode = "update";
                this.albumModal = true;
            } else {
                this.albumMode = "";
                this.albumModal = false;
            }
        },
        async updateTrack() {
            if(this.trackMode != "update") {
                this.trackMode = "update";
                this.trackModal = true;
            } else {
                this.trackMode = "";
                this.trackModal = false;
            }
        },
        async deleteArtist() {
            if(this.artistMode != "delete") {
                this.artistMode = "delete";
                this.artistModal = true;
            } else {
                this.artistMode = "";
                this.artistModal = false;
            }
        },
        async deleteGenre() {
            if(this.genreMode != "delete") {
                this.genreMode = "delete";
                this.genreModal = true;
            } else {
                this.genreMode = "";
                this.genreModal = false;
            }
        },
        async deleteAlbum() {
            if(this.albumMode != "delete") {
                this.albumMode = "delete";
                this.albumModal = true;
            } else {
                this.albumMode = "";
                this.albumModal = false;
            }
        },
        async deleteTrack() {
            if(this.trackMode != "delete") {
                this.trackMode = "delete";
                this.trackModal = true;
            } else {
                this.trackMode = "";
                this.trackModal = false;
            }
        },

        async handleArtist() {
            let response;
            let data = {
                "name" : this.artistName,
                "image" : this.artistImage,
                'admin_role' : this.role,
                'admin_token' : this.token
            }

            let baseURL = "http://127.0.0.1:5000/admin/artist";
            switch (this.artistMode) {
                case "create" :
                    response = await fetch(baseURL, this.buildRequest("POST", data));
                    break;
                case "update" : 
                    response = await fetch(baseURL + "/update", this.buildRequest("PUT", data));
                    break;
                case "delete" :
                    response = await fetch(baseURL + "/delete", this.buildRequest("DELETE", data));
                    break;
            }

            if(response.ok) {
                this.information = true;
                this.informationString = `Successfully applied ${this.artistMode}`;
                setTimeout(() => { 
                    this.artistMode = '';
                    this.artistModal = false;
                    this.clean();
                }, 500);
            }
        },
        async handleGenre() {
            let response;
            let data = {
                "genre_name" : this.newGenreName,
                "new_genre" : this.oldGenreName,
                'admin_role' : this.role,
                'admin_token' : this.token
            }
            let baseURL = "http://127.0.0.1:5000/admin/genre";

            switch (this.genreMode) {
                case "create" :
                    response = await fetch(baseURL, this.buildRequest("POST", data));
                    break;
                case "update" : 
                    response = await fetch(baseURL + "/update", this.buildRequest("PUT", data));
                    break;
                case "delete" :
                    response = await fetch(baseURL + "/delete", this.buildRequest("DELETE", data));
                    break;
            }

            if(response.ok) {
                this.information = true;
                this.informationString = `Successfully applied ${this.genreMode}`;
                setTimeout(() => { 
                    this.genreMode = '';
                    this.genreModal = false;
                    this.clean();
                }, 500);
            }
        },
        async handleAlbum() {
            let response;
            let data = {
                "album_id" : this.albumId,
                "name" : this.albumName,
                "release_date" : this.albumRelease,
                "image" : this.albumImage,
                "artist_name" : this.artistName,
                'admin_role' : this.role,
                'admin_token' : this.token
            }
            let baseURL = "http://127.0.0.1:5000/admin/album";

            switch (this.albumMode) {
                case "create" :
                    response = await fetch(baseURL, this.buildRequest("POST", data));
                    break;
                case "update" : 
                    response = await fetch(baseURL + "/update", this.buildRequest("PUT", data));
                    break;
                case "delete" :
                    response = await fetch(baseURL + "/delete", this.buildRequest("DELETE", data));
                    break;
            }

            if(response.ok) {
                this.information = true;
                this.informationString = `Successfully applied ${this.albumMode}`;
                setTimeout(() => { 
                    this.genreMode = '';
                    this.genreModal = false;
                    this.clean();
                }, 500);
            }
        },
        async handleTrack() {
            let response;
            let data = {
                "track_id" : this.trackId,
                "name" : this.trackName,
                "duration" : this.trackDuration,
                "file_path" : this.trackPath,
                "album_id" : this.albumId,
                'admin_role' : this.role,
                'admin_token' : this.token
            }
            let baseURL = "http://127.0.0.1:5000/admin/track";

            switch (this.trackMode) {
                case "create" :
                    response = await fetch(baseURL, this.buildRequest("POST", data));
                    break;
                case "update" : 
                    response = await fetch(baseURL + "/update", this.buildRequest("PUT", data));
                    break;
                case "delete" :
                    response = await fetch(baseURL + "/delete", this.buildRequest("DELETE", data));
                    break;
            }

            if(response.ok) {
                this.information = true;
                this.informationString = `Successfully applied ${this.trackMode}`;
                setTimeout(() => { 
                    this.genreMode = '';
                    this.genreModal = false;
                    this.clean();
                }, 500);
            }
        },

        clean() {
            this.adminModal = false;
            this.artistModal = false;
            this.genreModal = false;
            this.albumModal = false;
            this.trackModal = false;
            this.information = false;
            this.error = false;
        },
        buildRequest(type, data) {
            return {method: type,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)};
        }

    },
    template:
    `
    <div v-if="signedIn">
        <div>
            <button @click="adminModal = !adminModal"> Add a new admin </button>
            <button @click="createNewArtist()" > Add new artist </button>
            <button @click="updateArtist()" > Update an artist </button>
            <button @click="deleteArtist()" > Delete an artist </button>
            <button @click="createNewGenre()"> Add a genre </button>
            <button @click="updateGenre()"> Update a genre </button>
            <button @click="deleteGenre()"> Delete a genre </button>
            <button @click="createNewAlbum()"> Add new album </button>
            <button @click="updateAlbum()"> Update an album </button>
            <button @click="deleteAlbum()"> Delete an album </button>
            <button @click="createNewTrack()"> Add a track </button>
            <button @click="updateTrack()"> Update a track </button>
            <button @click="deleteTrack()"> Delete a track </button>
        </div>
        <p v-if="error" style="color:red"> {{errorString}} </p>
        <p v-if="information"> {{informationString}} </p>

        <div v-if="adminModal">
            <form @submit.prevent="registerAdmin()">
                <label> Username </label><br>
                <input v-model="newAdminUsername" /><br>
                <label> Password </label><br>
                <input v-model="newAdminPass" type="password" /> <br>
                <label> Email </label><br>
                <input v-model="newAdminEmail" /><br>
                <label> Date Of Birth </label><br>
                <input v-model="newAdminDOB" type="date" /><br>
                <label> Registration Key </label><br>
                <input v-model="regKey" type="password" /><br>
                <button type="submit"> Submit! </button>
            </form>
        </div>

        <div v-if="artistModal">
            <form @submit.prevent="handleArtist()">
                <label> Artist Name </label><br>
                <input v-model="artistName" /><br>
                <label v-if="artistMode!='delete'"> Arist Image </label> <br>
                <input v-if="artistMode!='delete'" v-model="artistImage" /> <br>
                <button> Execute </button>
            </form>
        </div>

        <div v-if="genreModal">
            <form @submit.prevent="handleGenre()">
                <label> Genre Name </label>
                <input v-model="newGenreName" />
                <label v-if="genreMode=='update'"> New Genre Name </label> 
                <input v-if="genreMode=='update'" v-model="oldGenreName" />
                <button type="submit"> Submit </button>
            </form>
        </div>

        <div v-if="albumModal">
            <form @submit.prevent="handleAlbum()">
                <label v-if="albumMode!='create'"> Album ID to update </label><br v-if="albumMode!='create'">
                <input v-if="albumMode!='create'" v-model="albumId"/><br v-if="albumMode!='create'">
                <div v-if="albumMode!='delete'">
                    <label> Album Name </label><br>
                    <input v-model="albumName" /><br>
                    <label> Release Date </label><br>
                    <input v-model="albumRelease" type="date" /><br>
                    <label> Image </label><br>
                    <input v-model="albumImage" /><br>
                    <label> Artist Name </label><br>
                    <input v-model="artistName" /><br>
                </div>
                <button type="submit"> Submit </button>
            </form>
        </div>

        <div v-if="trackModal">
            <form @submit.prevent="handleTrack()">
                <label v-if="trackMode!='create'"> Track Id </label><br v-if="trackMode!='create'">
                <input v-if="trackMode!='create'" v-model="trackId"/><br v-if="trackMode!='create'">
                <div v-if="trackMode!='delete'">
                    <label> Track Name </label><br>
                    <input v-model="trackName"/><br>
                    <label> Track Duration </label><br>
                    <input v-model="trackDuration"/><br>
                    <label> Path to listen to track </label><br>
                    <input v-model="trackPath" /><br>
                    <label> Album ID </label><br>
                    <input v-model="albumId" /><br>
                </div>
                <button type="submit"> Submit </button>
            </form>
        </div>


    </div>
    <div v-if="!signedIn">
        <form @submit.prevent="loginAdmin()">
            <label> Username </label><br>
            <input v-model="username" /><br>
            <label> Password </label><br>
            <input v-model="password" type="password" /><br>
            <label> Registration Key </label><br>
            <input v-model="regKey" type="password" /><br>
            <button type=submit> Sign In! </button>
        </form>
    </div>
    `

}