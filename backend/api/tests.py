from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import EquipmentDataset


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
    
    def test_user_registration(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
    
    def test_user_login(self):
        # Create user first
        User.objects.create_user(username='testuser', password='testpass123')
        
        # Login
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


class DatasetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.upload_url = '/api/datasets/upload/'
    
    def test_dataset_creation(self):
        dataset = EquipmentDataset.objects.create(
            user=self.user,
            filename='test.csv',
            raw_data=[{'Equipment Name': 'Test', 'Type': 'Pump', 'Flowrate': 100, 'Pressure': 50, 'Temperature': 25}],
            summary_stats={'total_count': 1},
            row_count=1,
            equipment_types=['Pump']
        )
        self.assertEqual(dataset.user, self.user)
        self.assertEqual(dataset.filename, 'test.csv')
    
    def test_dataset_cleanup(self):
        # Create 7 datasets
        for i in range(7):
            EquipmentDataset.objects.create(
                user=self.user,
                filename=f'test{i}.csv',
                raw_data=[],
                summary_stats={},
                row_count=0,
                equipment_types=[]
            )
        
        # Should only keep 5 newest
        count = EquipmentDataset.objects.filter(user=self.user).count()
        self.assertEqual(count, 5)
