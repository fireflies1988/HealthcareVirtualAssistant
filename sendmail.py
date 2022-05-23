import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "n18dccn237java@gmail.com"  # Enter your address nqubjcnsenjyrppp
receiver_email = "thienthien20221@gmail.com"  # Enter receiver addresspassword
password="dqocoxgxjylgooqg"
#password = input("Type your password and press enter: ")
# message = """\
# Subject: Hi doctor
#
# Patient is showing signs of poor health. their heart rate is: """




def sendemail(port, sender_email, receiver_email, password,message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


# # Run
# sendemail(port, sender_email, receiver_email, password, message)
# print("Status: Exit")