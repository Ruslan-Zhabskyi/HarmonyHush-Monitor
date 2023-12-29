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

// Get a reference to the database service
const database = firebase.database();

// Create a reference to the "data" path in your database
const dataRef = database.ref("data");

// Specify the Glitch app file location
const glitchAppFileLocation = "models/all_data.json";

// Fetch data from Firebase Realtime Database
dataRef.once("value")
  .then(snapshot => {
    // Convert the snapshot to JSON
    const data = snapshot.val();

    // Store the data in your Glitch app at the specified location
    // This assumes you have a function to write to a file in your Glitch app
    writeDataToFileInGlitch(data, glitchAppFileLocation);
  })
  .catch(error => {
    console.error("Error fetching data:", error);
  });

// Function to write data to a file in Glitch app
function writeDataToFileInGlitch(data, fileLocation) {
  // Implement the logic to write data to a file in your Glitch app
  // This depends on the capabilities and environment of your Glitch app
  // You may need to use Glitch's file system or an external storage service
  // Here's a basic example using localStorage (note: localStorage may have size limitations)
  localStorage.setItem(fileLocation, JSON.stringify(data));
}
