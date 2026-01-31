from rest_framework import serializers
from django.contrib.auth.models import User
from .models import EquipmentDataset


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    """Serializer for EquipmentDataset model"""
    user = UserSerializer(read_only=True)
    uploaded_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'user', 'filename', 'uploaded_at', 'raw_data', 
                  'summary_stats', 'row_count', 'equipment_types']
        read_only_fields = ['id', 'user', 'uploaded_at', 'raw_data', 
                           'summary_stats', 'row_count', 'equipment_types']


class DatasetSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for dataset list/history"""
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'filename', 'uploaded_at', 'row_count']


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload"""
    file = serializers.FileField()
    
    def validate_file(self, value):
        # Check file extension
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Check file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("File size cannot exceed 5MB.")
        
        return value
