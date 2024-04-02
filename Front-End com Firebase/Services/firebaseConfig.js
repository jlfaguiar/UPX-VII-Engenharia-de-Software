// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, initializeAuth, getReactNativePersistence } from "firebase/auth";
import { getFirestore } from 'firebase/firestore';
import { ReactNativeAsyncStorage } from '@react-native-async-storage/async-storage';

// const firebaseConfig = {
//   apiKey: "AIzaSyBewH46Y1TiuY-4x0oi5Raqg663-ZfjQOk",
//   authDomain: "agendavagas.firebaseapp.com",
//   projectId: "agendavagas",
//   storageBucket: "agendavagas.appspot.com",
//   messagingSenderId: "594620942785",
//   appId: "1:594620942785:web:d3d81c5e776304c373c740",
//   measurementId: "G-XJ7S8PKMPG"
// };

const firebaseConfig = {
  apiKey: "AIzaSyDCGer-BMR3TaoNAiXd_23EB2eDEZ5IlYk",
  authDomain: "facens-caronas.firebaseapp.com",
  projectId: "facens-caronas",
  storageBucket: "facens-caronas.appspot.com",
  messagingSenderId: "50689259717",
  appId: "1:50689259717:web:63394ee6bde4c14d7b58ac",
  measurementId: "G-EGRJLPPMQW"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const db = getFirestore(app);
// const auth = getAuth(app);
const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(ReactNativeAsyncStorage)
});



export {auth, db}