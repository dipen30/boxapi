from box import client

c = client.BoxClient("Access Token")

f = open("1.jpg", "rb")
files = c.upload_file(f, "folder Id")
f.close()
print files

file_content = c.download_file("file Id")
f = open("1.jpg", "wb")
f.write(file_content.read())
file_content.close()
f.close()

