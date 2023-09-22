import math

def calculate_solar_elevation(latitude, day_of_year, hour_of_day):
    """
    Calculate solar elevation angle in degrees.

    Parameters:
    latitude (float): Latitude in degrees (positive for Northern Hemisphere, negative for Southern Hemisphere).
    day_of_year (int): Day of the year (1-365).
    hour_of_day (float): Hour of the day in decimal form (0-24).

    Returns:
    float: Solar elevation angle in degrees.
    """
    # Convert latitude to radians
    lat_rad = math.radians(latitude)

    # Calculate the declination angle (δ) in radians
    declination = 23.45 * math.radians(math.sin(math.radians(360 / 365 * (day_of_year - 81))))

    # Calculate the solar hour angle (H) in radians
    solar_hour_angle = math.radians(15 * (hour_of_day - 12))

    # Calculate the argument for asin
    sin_arg = math.sin(lat_rad) * math.sin(declination) + math.cos(lat_rad) * math.cos(declination) * math.cos(solar_hour_angle)

    # Ensure that sin_arg stays within the valid range [-1, 1]
    sin_arg = max(min(sin_arg, 1), -1)

    # Calculate solar elevation angle (h) in radians
    solar_elevation_rad = math.asin(sin_arg)

    # Convert solar elevation angle to degrees
    solar_elevation_deg = math.degrees(solar_elevation_rad)

    return solar_elevation_deg

# Example usage:
latitude = 37.7749  # San Francisco's approximate latitude
day_of_year = 180  # Example: July 1st
hour_of_day = 12.0  # Example: Noon
elevation_angle = calculate_solar_elevation(latitude, day_of_year, hour_of_day)
print(f"Solar Elevation Angle: {elevation_angle} degrees")




def calculate_day_length(latitude, day_of_year):

    # Calculate the solar declination angle (δ) in radians
    declination = math.radians(23.45) * math.sin(math.radians(360 / 365 * (day_of_year - 81)))

    # Calculate the hour angles at sunrise and sunset (H0) in radians
    lat_rad = math.radians(latitude)
    
    # Calculate the value inside acos
    acos_arg = -math.tan(lat_rad) * math.tan(declination)
    
    # Ensure that acos_arg stays within the valid range [-1, 1]
    acos_arg = max(min(acos_arg, 1), -1)
    
    # Calculate the length of the day (in hours) as 2 times the hour angle at sunset
    H0 = math.acos(acos_arg)

    # Calculate day length in hours
    day_length_hours = 2 * math.degrees(H0) / 15.0

    # Handle cases where day length is 24 hours (continuous daylight)
    if day_length_hours >= 24:
        day_length_hours = 24

    return day_length_hours


def continuous_precipitation(latitude, day_of_year):
    """
    Approximate continuous precipitation based on latitude and day of the year.

    Parameters:
    latitude (float): Latitude in degrees (positive for Northern Hemisphere, negative for Southern Hemisphere).
    day_of_year (int): Day of the year (1-365).

    Returns:
    float: Approximated precipitation value (in mm) for the given location and date.
    """
    # Define functions to model precipitation variation throughout the year.
    # You can adjust the parameters to fit your desired patterns.
    seasonal_precipitation_amplitude = 15  # Amplitude of the seasonal variation
    annual_precipitation_average = 20  # Average annual precipitation

    # Calculate the angular frequency for the annual cycle
    omega = 2 * math.pi / 365

    # Calculate the latitude factor to model higher precipitation near the equator
    latitude_factor = math.cos(math.radians(latitude))

    # Calculate the precipitation value based on latitude, day of the year, and functions
    precipitation = (
        annual_precipitation_average
        + seasonal_precipitation_amplitude * latitude_factor * math.sin(omega * day_of_year)
    )

    # Ensure that precipitation values are non-negative
    precipitation = max(precipitation, 0)

    return precipitation


# Check if the script is being run as the main program
if __name__ == "__main__":
    latitude = 80  
    day_of_year = 120  
    hour_of_day = 12.0 

    elevation_angle = calculate_solar_elevation(latitude, day_of_year, hour_of_day)
    print(f"Solar Elevation Angle: {elevation_angle} degrees")

    day_length = calculate_day_length(latitude, day_of_year)
    print(f"Day Length: {day_length} hours")
    
    precip = continuous_precipitation(latitude, day_of_year)
    print(f"Precipitation: {precip} mm")
    
    