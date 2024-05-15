from .models import Driver, User, Ride
from rest_framework.response import Response
from rest_framework import status
from .serializer import driverSerializer, userSerializer, rideSerializer
from rest_framework.views import APIView
from django.http import Http404
from geopy.distance import geodesic

class crudDriver(APIView):
    def get(self, request):
        driver_id = request.query_params.get("driverID")
        try:
            driver = Driver.objects.get(driverID=driver_id)
            serializer = driverSerializer(driver)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Driver.DoesNotExist:
            raise Http404("Driver does not exist")
    
    def post(self, request):
        try:
            serializer = driverSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return(Response(serializer.data, status=status.HTTP_201_CREATED))
        except:
            return(Response("Driver already exists", status=status.HTTP_400_BAD_REQUEST))
    
    def delete(self, request):
        driver_id = request.query_params.get("driverID")
        driver = Driver.objects.get(driverID=driver_id)
        serializer = driverSerializer(driver)
        driver.delete()
        return(Response(data=serializer.data,status=status.HTTP_200_OK))
    
    def put(self, request):
        driver_id = request.data.get("driverID")
        try:
            driver = Driver.objects.get(driverID=driver_id)
        except Driver.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
        fields_to_update = ["password", "latitude", "longitude", "available"]
        for field in fields_to_update:
            if field in request.data:
                setattr(driver, field, request.data[field])
        driver.save()
        serializer = driverSerializer(driver)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class crudUser(APIView):
    def get(self, request):
        user_id = request.query_params.get("userID")
        Email = request.query_params.get("email")
        Password = request.query_params.get("password")
        try:
            if user_id:
                user = User.objects.get(userID=user_id)
                serializer = userSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif Email and Password:
                user = User.objects.filter(email=Email, password=Password).first()
                if user:
                    serializer = userSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("User with provided email and password does not exist", status=status.HTTP_404_NOT_FOUND)
            elif Email:
                user = User.objects.filter(email=Email).first()
                if user:
                    serializer = userSerializer(user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("User with provided email does not exist", status=status.HTTP_404_NOT_FOUND)
            else:
                return Response("Invalid request parameters", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_404_NOT_FOUND)

    
    def post(self, request):
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return(Response(serializer.data, status=status.HTTP_201_CREATED))
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
    
    def delete(self, request):
        user_id = request.query_params.get("userID")
        user = User.objects.get(userID=user_id)
        serializer = userSerializer(user)
        user.delete()
        return(Response(serializer.data, status=status.HTTP_200_OK))
    
    def put(self, request):
        user_id = request.data.get("userID")
        try:
            user = User.objects.get(userID=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if "password" in request.data:
            setattr(user, "password", request.data["password"])
        user.save()
        serializer = userSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class crudRides(APIView):
    def get(self, request):
        ride_id = request.query_params.get("rideID")
        user_id = request.query_params.get("userID")
        if ride_id:
            try:
                ride = Ride.objects.get(rideID = ride_id)
                serializer = rideSerializer(ride)
                return(Response(serializer.data, status=status.HTTP_200_OK))
            except:
                raise Http404("Ride does not exist")
        elif user_id:
            try:
                user = User.objects.filter(userID = user_id)
                serializer = userSerializer(user, many=True)
                return(Response(serializer.data, status=status.HTTP_200_OK))
            except:
                raise Http404("User does not exist")

    
    def post(self, request):
        serializer = rideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return(Response(serializer.data, status=status.HTTP_201_CREATED))
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))
    
    def delete(self, request):
        ride_id = request.query_params.get("rideID")
        ride = Ride.objects.get(rideID = ride_id)
        serializer = rideSerializer(ride)
        ride.delete()
        return(Response(serializer.data, status=status.HTTP_200_OK))
    
class crudAssigner(APIView):
    def get(self, request):
        pickup_latitude = float(request.query_params.get("latitude"))
        pickup_longitude = float(request.query_params.get("longitude"))
        vehicleType = request.query_params.get("vehicle_type")
        
        drivers = Driver.objects.filter(available=True, vehicle_type=vehicleType)
        
        for driver in drivers:
            distance = geodesic((pickup_latitude, pickup_longitude), (driver.latitude, driver.longitude)).meters
            driver.distance = distance
        drivers = sorted(drivers, key=lambda x: (x.distance, x.rating), reverse=False)[:5]
        serializer = driverSerializer(drivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    





'''
# Create your views here.
def getNearestDriver(request, userLatitude, userLongitude):
    drivers = Driver.objects.all()
    if request.method == 'GET':
        for driver in drivers:
            if driver.is_available:
                driver.distance = (((userLatitude - driver.latitude)**2) + ((userLongitude - driver.longitude)**2))**0.5
            else:
                driver.distance = float('inf')
        drivers = sorted(drivers, key=lambda x: x.distance)
        return(Response(data=drivers[:5], status=status.HTTP_200_OK))
    return(Response(status=status.HTTP_405_METHOD_NOT_ALLOWED))

@api_view(['POST'])
def addDriver(request, id, is_available, latitude, longitude, vehicle_type):
    if request.method == 'POST':
        serializer = driverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return(Response(serializer.data, status=status.HTTP_201_CREATED))
    return(Response(status=status.HTTP_405_METHOD_NOT_ALLOWED))

def updateDriver(request, id, latitude, longitude):
    if request.method == 'PUT':
        driver = Driver.objects.get(id)
        driver.latitude = latitude
        driver.longitude = longitude
        driver.save()
        return(Response(data=driver, status=status.HTTP_200_OK))
    return(Response(status=status.HTTP_405_METHOD_NOT_ALLOWED))
'''
