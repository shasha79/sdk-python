import requests, json

class DirectusClient:

    def __init__(self, url, project, email=None, password=None):
        self.url = url + '/' + project
        self.email = email
        self.password = password
        self.project = project
        self.access = None

        if email is not None and password is not None:

            payload = {
                "email": email,
                "password": password
            }

            combined_url = self.url + '/auth/authenticate'
            r = requests.post(combined_url, data=payload)
            data = r.json() 

            self.access = data['data']["token"]

    def refresh_token(self, ):
        combined_url = self.url + '/auth/refresh'
        r = requests.post(combined_url, data={"token": self.access})
        data = r.json()
        self.access = data['data']["token"]


    def get_items_list(self, collection, limit=200):
        """Function list items from collection. 
        
        Parameters
        ----------
        collection : str
            collection name
        limit : int
            A limit on the number of objects that are returned. Default is 200.
            To grab all items from collection pass: `-1`, but be careful this could take a lot of time.
            
                    
        Original method description:
        https://docs.directus.io/api/items.html#list-the-items
        """
        headers = {"Authorization": "Bearer " + self.access}
        return requests.get(self.url + "/items/" + collection + "?limit=" + str(limit), headers=headers).json()

    def get_item(self, collection, id, fields="*"):
        """Function get item from collection. 
        
        Parameters
        ----------
        collection : str
            collection name
        id : str or int
            id of the item
        fields : str, optional
            Special sign to select only needed fields. 
            Popular options are: 
            `*` - default. Get all top-level fields. 
            `*.*` - Get all top-level fields and all second-level relational fields.
            `*,images.*` - Get all top-level fields and second-level relational fields within images
            
            All signs could be founded here: 
            https://docs.directus.io/api/query/fields.html
            
        Original method description:
        https://docs.directus.io/api/items.html#retrieve-an-item
        """
        
        headers = {"Authorization": "Bearer " + self.access}
        return requests.get(self.url + "/items/" + collection + "/" + str(id)+"?fields="+str(fields), headers=headers).json()

    def create_item(self, collection, item):
        headers = {"Authorization": "Bearer " + self.access}
        return requests.post(self.url + "/items/" + collection, data=item, headers=headers)

    def get_files_list(self):
        headers = {"Authorization": "Bearer " + self.access}
        return requests.get(self.url + "/files", headers=headers).json() 

    def get_file(self, id):
        headers = {"Authorization": "Bearer " + self.access}
        return requests.get(self.url + "/files/" + str(id), headers=headers).json()
