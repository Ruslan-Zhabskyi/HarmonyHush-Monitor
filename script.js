// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBqq5uFvuul59UZKh_7_WDHM0i3e5w6EZg",
  authDomain: "harmonyhushmonitor.firebaseapp.com",
  databaseURL: "https://harmonyhushmonitor-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "harmonyhushmonitor",
  storageBucket: "harmonyhushmonitor.appspot.com",
  messagingSenderId: "353494293835",
  appId: "1:353494293835:web:ee78564b64148bcbcc9cce",
  measurementId: "G-DBZ6NYWCK4"
};

firebase.initializeApp(firebaseConfig);

// Get a reference to the file storage service
const storage = firebase.storage();
// Get a reference to the database service
const database = firebase.database();

// Create camera database reference
const camRef = database.ref("file");

// Sync on any updates to the DB. THIS CODE RUNS EVERY TIME AN UPDATE OCCURS ON THE DB.
camRef.limitToLast(1).on("value", function(snapshot) {
  snapshot.forEach(function(childSnapshot) {
    const image = childSnapshot.val()["image"];
    const time = childSnapshot.val()["timestamp"];
    const storageRef = storage.ref(image);

    storageRef
      .getDownloadURL()
      .then(function(url) {
        console.log(url);
        document.getElementById("photo").src = url;
        document.getElementById("time").innerText = time;
      })
      .catch(function(error) {
        console.log(error);
      });
  });
});