import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyB9O5m92e395fNLlFzqUF7xTmNBtUcxb4c",
  "authDomain": "nhung-c3e4e.firebaseapp.com",
  "databaseURL": "https://nhung-c3e4e-default-rtdb.firebaseio.com",
  "projectId": "nhung-c3e4e",
  "storageBucket": "nhung-c3e4e.appspot.com",
  "messagingSenderId": "847152446523",
  "appId": "1:847152446523:web:db274ff6fc2c6e8ed6f01e",
  "measurementId": "G-2404E27MXC"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

