// Import the functions you need from the Firebase SDK
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";
import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";

  // Your web app's Firebase configuration
  const firebaseConfig = {
    apiKey: "AIzaSyBxuHJPQsKTzumuU-XPeUeG-zLTZug3F1M",
    authDomain: "memorialgym-f5ce3.firebaseapp.com",
    databaseURL: "https://memorialgym-f5ce3-default-rtdb.firebaseio.com",
    projectId: "memorialgym-f5ce3",
    storageBucket: "memorialgym-f5ce3.appspot.com",
    messagingSenderId: "567780843830",
    appId: "1:567780843830:web:c9c04ad30289df71d91397"
  };
const app = initializeApp(firebaseConfig);
const auth = getAuth();
const database = getDatabase();

// Function to handle user signup
function SignUp(e) {
  e.preventDefault();

  const fullName = document.getElementById("fullname").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("copassword").value;

  // Validate input fields
  if (!fullName || !email || !password || !confirmPassword) {
    alert("All fields are required");
    return;
  }

  if (password !== confirmPassword) {
    alert("Password confirmation does not match");
    return;
  }

  // Create user with email and password
  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // User signed up successfully
      const user = userCredential.user;

      // Save user details to the database
      const userRef = ref(database, 'users/' + user.uid);
      set(userRef, {
        fullName: fullName,
        email: email
      })
        .then(() => {
          alert("Sign up successful!");
          window.location.href = 'login.html'; // Redirect to login page
        })
        .catch((error) => {
          console.error("Error saving user data: ", error.message);
        });
    })
    .catch((error) => {
      alert("Error signing up: " + error.message);
    });
}

// Attach SignUp function to the signup form submission
const signupForm = document.querySelector("form");
if (signupForm) {
  signupForm.addEventListener("submit", SignUp);
} else {
  console.error("Signup form not found.");
}
