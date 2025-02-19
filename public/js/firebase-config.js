import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getFirestore, collection, addDoc, serverTimestamp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyAFFldEP4nCA4XU3AvJ6FcDy6mY0eBnke0",
  authDomain: "kuantum-server.firebaseapp.com",
  projectId: "kuantum-server",
  storageBucket: "kuantum-server.firebasestorage.app",
  messagingSenderId: "13997661825",
  appId: "1:13997661825:web:64cc3e11b8c2ccf7707780"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { app, db, collection, addDoc, serverTimestamp };
