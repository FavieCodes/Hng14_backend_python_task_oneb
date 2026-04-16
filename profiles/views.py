import uuid
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer, ProfileListSerializer
from .services import fetch_genderize_data, fetch_agify_data, fetch_nationalize_data

def api_documentation(request):
    """Render the API documentation page"""
    return render(request, 'api_docs.html')

@api_view(['GET', 'POST'])
def profile_list_create(request):
    """
    Handle both:
    - GET: List all profiles with optional filtering
    - POST: Create a new profile by integrating data from three external APIs
    """
    
    # GET request - list all profiles
    if request.method == 'GET':
        profiles = Profile.objects.all()
        
        # Apply filters (case-insensitive)
        gender = request.query_params.get('gender', '').strip()
        if gender:
            profiles = profiles.filter(gender__iexact=gender)
        
        country_id = request.query_params.get('country_id', '').strip()
        if country_id:
            profiles = profiles.filter(country_id__iexact=country_id)
        
        age_group = request.query_params.get('age_group', '').strip()
        if age_group:
            profiles = profiles.filter(age_group__iexact=age_group)
        
        # Serialize with simplified serializer
        serializer = ProfileListSerializer(profiles, many=True)
        return Response({
            'status': 'success',
            'count': profiles.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    # POST request - create new profile
    elif request.method == 'POST':
        # Validate request body
        if 'name' not in request.data:
            return Response(
                {'status': 'error', 'message': 'Missing or empty name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        name = request.data.get('name', '').strip().lower()
        
        if not name:
            return Response(
                {'status': 'error', 'message': 'Missing or empty name'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(name, str):
            return Response(
                {'status': 'error', 'message': 'Invalid type'},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if profile already exists
        existing_profile = Profile.objects.filter(name=name).first()
        if existing_profile:
            serializer = ProfileSerializer(existing_profile)
            return Response({
                'status': 'success',
                'message': 'Profile already exists',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        # Fetch data from external APIs
        gender_data, gender_error = fetch_genderize_data(name)
        if gender_error:
            return Response(
                {'status': 'error', 'message': gender_error},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        age_data, age_error = fetch_agify_data(name)
        if age_error:
            return Response(
                {'status': 'error', 'message': age_error},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        country_data, country_error = fetch_nationalize_data(name)
        if country_error:
            return Response(
                {'status': 'error', 'message': country_error},
                status=status.HTTP_502_BAD_GATEWAY
            )
        
        # Create profile
        profile = Profile.objects.create(
            name=name,
            **gender_data,
            **age_data,
            **country_data
        )
        
        serializer = ProfileSerializer(profile)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE'])
def profile_detail_delete(request, profile_id):
    """
    Handle both:
    - GET: Get a single profile by ID
    - DELETE: Delete a profile by ID
    """
    
    # Validate UUID format
    try:
        uuid_obj = uuid.UUID(profile_id)
    except ValueError:
        return Response(
            {'status': 'error', 'message': 'Profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # GET request - fetch single profile
    if request.method == 'GET':
        profile = get_object_or_404(Profile, id=uuid_obj)
        serializer = ProfileSerializer(profile)
        return Response({
            'status': 'success',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    # DELETE request - delete profile
    elif request.method == 'DELETE':
        profile = get_object_or_404(Profile, id=uuid_obj)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)