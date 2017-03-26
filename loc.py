from geopy.geocoders import Nominatim
geolocator = Nominatim()
location = geolocator.reverse("37.42805,-122.16791")
print(location.address)
