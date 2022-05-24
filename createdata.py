# import pyrebase
#
# #Initialize Firebase
# firebaseConfig={"apiKey" : "AIzaSyB9O5m92e395fNLlFzqUF7xTmNBtUcxb4c" ,
#   "authDomain" : "nhung-c3e4e.firebaseapp.com" ,
#   "databaseURL" : "https://nhung-c3e4e-default-rtdb.firebaseio.com" ,
#   "projectId" : "nhung-c3e4e" ,
#   "storageBucket" : "nhung-c3e4e.appspot.com" ,
#   "messagingSenderId" : "847152446523" ,
#   "appId" : "1:847152446523:web:db274ff6fc2c6e8ed6f01e" ,
#   "measurementId" : "G-2404E27MXC"}
#
# firebase=pyrebase.initialize_app(firebaseConfig)
#
# db=firebase.database()
#
# #Push Data
# data={"age":20, "address":["new york", "los angeles"]}
# print(db.push(data)) #unique key is generated
#
# #Create paths using child
# #data={"name":"Jane", "age":20}
# #db.child("Branch").child("Employees").push(data)
#
# #Create your own key
# data={"age":20, "address":["new york", "los angeles"]}
# db.child("John").set(data)
#
# #Create your own key + paths with child
# data={"name":"John", "age":20, "address":["new york", "los angeles"]}
# db.child("Branch").child("Employee").child("male employees").child("John's info").set(data)
#
#
#
