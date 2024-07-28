import smtplib
# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login("mamlesh.va06@gmail.com", "nkdh bwyg seks qvni")
# message to be sent
message = "Message_you_need_to_send"
# sending the mail
s.sendmail("mamlesh.va06@gmail.com", "mamlesh.va06@gmail.com", message)
# te