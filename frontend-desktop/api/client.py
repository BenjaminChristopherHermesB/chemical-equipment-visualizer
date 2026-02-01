import requests
import json

class APIClient:
    """
    API client for communicating with the Django backend.
    """
    def __init__(self, base_url='https://chemical-equipment-backend-bhi7.onrender.com/api'):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.session = requests.Session()
    
    def _get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def register(self, username, email, password, password2):
        """Register a new user"""
        url = f'{self.base_url}/auth/register/'
        data = {
            'username': username,
            'email': email,
            'password': password,
            'password2': password2
        }
        response = self.session.post(url, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 201:
            try:
                result = response.json()
                self.token = result['token']
                return result
            except json.JSONDecodeError:
                raise Exception(f"Failed to decode response (Status {response.status_code}): {response.text[:100]}...")
        else:
            try:
                error_msg = response.json().get('error', 'Registration failed')
            except json.JSONDecodeError:
                error_msg = f"Request failed (Status {response.status_code}): {response.text[:100]}..."
            raise Exception(error_msg)
    
    def login(self, username, password):
        """Login and get authentication token"""
        url = f'{self.base_url}/auth/login/'
        data = {'username': username, 'password': password}
        response = self.session.post(url, json=data, headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            try:
                result = response.json()
                self.token = result['token']
                return result
            except json.JSONDecodeError:
                raise Exception(f"Failed to decode response (Status {response.status_code}): {response.text[:100]}...")
        else:
            try:
                error_msg = response.json().get('error', 'Login failed')
            except json.JSONDecodeError:
                error_msg = f"Request failed (Status {response.status_code}): {response.text[:100]}..."
            raise Exception(error_msg)
    
    def logout(self):
        """Logout and clear token"""
        if not self.token:
            return
        
        url = f'{self.base_url}/auth/logout/'
        try:
            self.session.post(url, headers=self._get_headers())
        except:
            pass
        finally:
            self.token = None
    
    def upload_csv(self, file_path):
        """Upload CSV file"""
        url = f'{self.base_url}/datasets/upload/'
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files, headers=headers)
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(response.json().get('error', 'Upload failed'))
    
    def get_datasets(self):
        """Get list of datasets"""
        url = f'{self.base_url}/datasets/'
        response = self.session.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to fetch datasets')
    
    def get_dataset(self, dataset_id):
        """Get specific dataset"""
        url = f'{self.base_url}/datasets/{dataset_id}/'
        response = self.session.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to fetch dataset')
    
    def get_summary(self, dataset_id):
        """Get dataset summary"""
        url = f'{self.base_url}/datasets/{dataset_id}/summary/'
        response = self.session.get(url, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to fetch summary')
    
    def download_pdf(self, dataset_id, save_path):
        """Download PDF report"""
        url = f'{self.base_url}/datasets/{dataset_id}/pdf/'
        response = self.session.get(url, headers=self._get_headers(), stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f. write(chunk)
            return True
        else:
            raise Exception('Failed to download PDF')
