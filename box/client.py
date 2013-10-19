# box
# Copyright 2013-2014 Dipen Patel
# See LICENSE for details.

import urllib
import httplib
import json

from error import ERRORCODES, BoxError
import mimetypes

BOX_API_VERSION = "/2.0"
BOX_API_URL = "api.box.com"
BOX_DOWNLOAD_URL = "dl.boxcloud.com"
BOX_API_UPLOAD_URL = "upload.box.com"


class BoxClient(object):
    def __init__(self, access_token=None, timeout=None):
        self.access_token = access_token
        self.timeout = timeout

    def user_info(self, userId="me"):
        """Get information of logged in user.
        
        Args:
            - userId : User id to get information
        
        Returns:
            returns dictionary of user information
            For more details, visit:
            http://developers.box.com/docs/#users            
        """
        return self.request("/users/"+userId)

    def get_folders(self, folderId, **args):
        """ Get list of folders in given folder including all metadata
        
        Args:
            - folderId : Folder id to get list of items
        
        Returns:
            - A dictionary containing the metadata of files/folers
            
            For more details, visit:
            http://developers.box.com/docs/#folders-folder-object
        """
        return self.request("/folders/"+folderId, qs_args=args)

    def get_folders_items(self, folderId, **args):
        """ Get list of folders in given folder without any other metadata
        
        Args:
            - folderId : Folder id to get list of items
        
        Returns:
            - A dictionary containing the list of files/folers
            
            For more details, visit:
            http://developers.box.com/docs/#folders-retrieve-a-folders-items
        """
        return self.request("/folders/"+folderId+'/items', qs_args=args)

    def create_folder(self, **post_data):
        """ Creates an Empty folder inside specified parent folder
        
        Args:
            post_data : Dictionary object containing Folder name and parent Id
                        e.g. {"name": "New folder", "parent":{"id": "0"}}
        
        Returns:
            - A full folder object is returned
            For more details, visit:
            http://developers.box.com/docs/#folders-create-a-new-folder
        """
        return self.request("/folders/", method='POST', post_args=post_data)

    def update_folder_info(self, folderId, **post_data):
        """update folder information
        
        Args:
            - folderId : folder's id to update information
            - post_data : parameter lists to update(in json format)
            
        Returns:
            - The updated folder is returned if the name is valid
            for more details, visit:
            http://developers.box.com/docs/#folders-update-information-about-a-folder
        """
        return self.request("/folders/"+folderId, method="PUT", post_args=post_data)

    def delete_folder(self, folderId, **qs_args):
        """Delete a folder with given id
        
        Args:
            - folderId : Folder id to delete
            - qs_args : dictionary object of optional parameter "recursive"
                        e.g. {"recursive": "true"}
        
        Returns:
            - returns an 204 status response if folder is deleted successfully.
        """
        return self.request("/folders/"+folderId, method='DELETE', qs_args=qs_args)

    def get_files(self, fileId, **args):
        """Get information about a file with given id
        
        Args:
            - fileId : File id to get information
            - args : dictionary object of optional parameter
        
        Returns:
            - A full file object is returned
            For more details, visit:
            http://developers.box.com/docs/#files-get            
        """
        return self.request("/files/"+fileId, qs_args=args)

    def download_file(self, fileId, **args):
        """download a file of given fileID
        
        Args:
            - args : optional arguments (Version id)
            
        Returns:
            - httplib.HTTPResponse that is the result of the request.
            close HttpResponse once file is downloaded.
        """
        return self.request("/files/"+fileId+"/content", qs_args=args)
    
    def upload_file(self, fileObj, parentId, fileId=None):
        """ upload a file to specified folder
        
        Args:
            - fileObj : file object
            - parentId : folder id where file need to upload
            - fileId : if wanted to update existing file in parentId
        
        Returns:
            - full file object is returned in json object if the ID is valid
            for more details, visit
            http://developers.box.com/docs/#files-upload-a-file
        """
        return self.request_upload(parentId, fileObj=fileObj, fileId=fileId)
    
    def delete_file(self, fileId):
        """Delete a file with given id
        
        Args:
            - fileId : File id to delete
        
        Returns:
            - returns an 204 status response if file is deleted successfully.
            for more details, visit
            http://developers.box.com/docs/#files-delete-a-file
        """
        return self.request("/files/"+fileId, method="DELETE")

    def get_file_comments(self, fileId):
        """Get comments of given file id
        
        Args:
            - fileId : File id to get comment
        
        Returns:
            - A collection of comment objects are returned.
                If there are no comments on the file, an empty comments array is returned.
            for more details, visit
            http://developers.box.com/docs/#files-view-the-comments-on-a-file
        """
        return self.request("/files/"+fileId+"/comments")

    def get_comments(self, commentId):
        """Get comments with given id
        
        Args:
            - commentId : Comment id to get
        
        Returns:
            - A full comment object is returned is the ID is valid and if the user has access to the comment.
            for more details, visit
            http://developers.box.com/docs/#comments-get-information-about-a-comment
        """
        return self.request("/comments/"+commentId)

    def add_comments(self, **post_data):
        """Add comments to given id
        
        Args:
            - post_data : Dictionary object containing type of Comment and message
                        e.g. {"item": {"type": "file", "id": "FILE_ID"}, "message": "YOUR_MESSAGE"}

        Returns:
            - The new comment object is returned. Errors may occur if the item id is invalid,
                the item type is invalid/unsupported, or if the user does not have access to the item being commented on.
            for more details, visit
            http://developers.box.com/docs/#comments-add-a-comment-to-an-item
        """
        return self.request("/comments/", method="POST", post_args=post_data)

    def edit_comment(self, commentId, **post_data):
        """Edit comments to given id
        
        Args:
            - commentId : id of comment to modify
            - post_data : Dictionary object containing new message
                        e.g. {message": "YOUR NEW MESSAGE"}

        Returns:
            - The full updated comment object is returned
                if the ID is valid and if the user has access to the comment.
            for more details, visit
            http://developers.box.com/docs/#comments-change-a-comments-message
        """
        return self.request("/comments/"+commentId, method="PUT", post_args=post_data)

    def delete_comment(self, commentId):
        """Delete comment of given id
        
        Args:
            - commentId : id of comment to delete

        Returns:
            - An empty 204 response is returned to confirm deletion of the comment.
                Errors can be thrown if the ID is invalid or if the user is not authorized to delete this particular comment.
            for more details, visit
            http://developers.box.com/docs/#comments-delete-a-comment
        """
        return self.request("/comments/"+commentId, method="DELETE")
    
    def search_items(self, **qs_args):
        """Search items in user's box account
        
        Args:
            - qs_args : Dictionary object containing search query, limit and offset
                        e.g. {"query": "football", "limit":1, "offset": 0}

        Returns:
            - A collection of search results is returned.
                If there are no matching search results, the entries array will be empty.
            for more details, visit
            http://developers.box.com/docs/#search-searching-a-users-account
        """
        return self.request("/search/", method="GET", qs_args=qs_args)

    def request_upload(self, parentId, method='POST', fileObj=None, fileId=None):
        """An internal method that builds the url, headers, and params for Box API request.
        
        Args:
            - path : API endpoint with leading slash
            - method : An HTTP method
            - qs_args : query sting arguments to send
            - post_args : POST data to send
        
        Returns:
            - return json or raw response based on API endpoint.
        """
        
        con = httplib.HTTPSConnection(BOX_API_UPLOAD_URL, timeout=self.timeout)
        
        if fileId:
            path = '/api/'+BOX_API_VERSION+'/files/'+fileId+'/content'
        else:    
            path = '/api/'+BOX_API_VERSION+'/files/content'

        headerValue = 'Bearer %s' % (self.access_token,)
        fields = {"filename": fileObj,"parent_id":parentId}
        content_type, body = self._encode_multipart_form(fields)

        headers = {
                   "Authorization": headerValue,
                   "Content-Type": content_type
                   }

        con.request(method, path, body, headers)
        response = {}

        data = con.getresponse()
        if data.status in ERRORCODES:
            response["status"] = data.status
            response["error"] = data.reason
        else:
            response = data.read()
        data.close()
        con.close()

        try:
            return json.loads(response)
        except Exception, e:
            try:
                return json.dumps(response)
            except:
                raise BoxError(e)

    # based on: http://code.activestate.com/recipes/146306/
    def _encode_multipart_form(self, fields):
        """Encode files as 'multipart/form-data'.

        Fields are a dict of form name-> value. For files, value should
        be a file object.

        Returns (content_type, body) ready for httplib.HTTP instance.

        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        for (key, value) in fields.items():
            L.append('--' + BOUNDARY)
            if hasattr(value, 'read') and callable(value.read):
                filename = getattr(value, 'name')
                L.append(('Content-Disposition: form-data;'
                          'name="%s";'
                          'filename="%s"') % (key, filename))
                L.append('Content-Type: %s' % (mimetypes.guess_type(filename)[0],))
                value = value.read()
            else:
                L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            if isinstance(value, unicode):
                value = value.encode('ascii')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

    def request(self, path, method='GET', qs_args=None, post_args=None):
        """An internal method that builds the url, headers, and params for Box API request.
        
        Args:
            - path : API endpoint with leading slash
            - method : An HTTP method
            - qs_args : query sting arguments to send
            - post_args : POST data to send
        
        Returns:
            - return json or raw response based on API endpoint.
        """
        qs_args = qs_args or {}
        post_data = json.dumps(post_args) if post_args else None
        
        con = httplib.HTTPSConnection(BOX_API_URL, timeout=self.timeout)
        
        path = BOX_API_VERSION+path
        url = '%s?%s' % (path, urllib.urlencode(qs_args))

        headerValue = 'Bearer %s' % (self.access_token,)
        headers = {"Authorization": headerValue}
        con.request(method, url, post_data, headers)
        response = {}

        data = con.getresponse()
        if data.status in ERRORCODES:
            response["status"] = data.status
            response["error"] = data.reason
        elif data.status == 201 or data.status == 200:
            response = data.read()
        elif data.status == 302:
            url = data.getheader("location", "")
            data.close()
            con.close()
            con1 = httplib.HTTPSConnection(BOX_DOWNLOAD_URL, timeout=self.timeout)
            con1.request(method, url[len("https://"+BOX_DOWNLOAD_URL):])
            return con1.getresponse()

        data.close()
        con.close()

        try:
            # To parse response returned by Box.com APIs
            return json.loads(response)
        except:
            try:
                # To parse response created by this library
                return json.dumps(response)
            except:
                # return raw response
                return response
