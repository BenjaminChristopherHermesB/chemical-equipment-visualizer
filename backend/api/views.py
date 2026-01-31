from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import EquipmentDataset
from .serializers import (
    EquipmentDatasetSerializer,
    DatasetSummarySerializer,
    CSVUploadSerializer,
    UserSerializer,
    UserRegistrationSerializer
)
from .utils import parse_csv_file, compute_summary_statistics, dataframe_to_dict, generate_pdf_report


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and return auth token.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate user and return auth token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Please provide both username and password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by deleting auth token.
    """
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EquipmentDatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing equipment datasets.
    Provides CRUD operations and custom actions for CSV upload and PDF generation.
    """
    serializer_class = EquipmentDatasetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only datasets belonging to the current user"""
        return EquipmentDataset.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Use lightweight serializer for list action"""
        if self.action == 'list':
            return DatasetSummarySerializer
        return EquipmentDatasetSerializer
    
    @action(detail=False, methods=['post'], serializer_class=CSVUploadSerializer)
    def upload(self, request):
        """
        Upload and process CSV file.
        POST /api/datasets/upload/
        """
        serializer = CSVUploadSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        csv_file = serializer.validated_data['file']
        
        try:
            # Parse CSV with pandas
            df = parse_csv_file(csv_file)
            
            # Compute summary statistics
            summary_stats = compute_summary_statistics(df)
            
            # Convert DataFrame to dict for JSON storage
            raw_data = dataframe_to_dict(df)
            
            # Get equipment types list
            equipment_types = df['Type'].unique().tolist()
            
            # Create dataset record
            dataset = EquipmentDataset.objects.create(
                user=request.user,
                filename=csv_file.name,
                raw_data=raw_data,
                summary_stats=summary_stats,
                row_count=len(df),
                equipment_types=equipment_types
            )
            
            # Serialize and return
            response_serializer = EquipmentDatasetSerializer(dataset)
            return Response({
                'message': 'CSV uploaded and processed successfully',
                'dataset': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': f'An error occurred while processing the file: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """
        Get summary statistics for a specific dataset.
        GET /api/datasets/{id}/summary/
        """
        dataset = self.get_object()
        return Response({
            'id': dataset.id,
            'filename': dataset.filename,
            'uploaded_at': dataset.uploaded_at,
            'row_count': dataset.row_count,
            'summary_stats': dataset.summary_stats
        })
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """
        Generate and download PDF report for a specific dataset.
        GET /api/datasets/{id}/pdf/
        """
        dataset = self.get_object()
        
        try:
            pdf_content = generate_pdf_report(dataset)
            
            response = HttpResponse(pdf_content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{dataset.filename}_report.pdf"'
            
            return response
        except Exception as e:
            return Response({
                'error': f'Error generating PDF: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request, *args, **kwargs):
        """
        List last 5 datasets for the current user.
        GET /api/datasets/
        """
        queryset = self.get_queryset()[:5]  # Only return last 5
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Simple health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'message': 'Chemical Equipment Parameter Visualizer API is running'
    })
