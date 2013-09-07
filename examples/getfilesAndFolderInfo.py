from box import client

c = client.BoxClient("Access Token")

user = c.user_info()
print user

args = {"limit":2, "offset":0}
folder = c.get_folders("id", **args)
print folder

args = {"name": "NewFolder123"}
folder = c.update_folder_info("id", **args)
print folder

folder  = c.get_folders_items("id")
print folder

args = {"recursive": "true"}
folder = c.delete_folder("id", **args);
print folder

files = c.get_files("id")
print files


