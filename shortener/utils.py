from user_agents import parse
from django.contrib.gis.geoip2 import GeoIP2

def get_client_ip(request):
    """Extract client IP from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_device_type(user_agent_string):
    """Parse device type from user agent"""
    user_agent = parse(user_agent_string)
    if user_agent.is_mobile:
        return 'Mobile'
    elif user_agent.is_tablet:
        return 'Tablet'
    elif user_agent.is_pc:
        return 'Desktop'
    else:
        return 'Unknown'

def get_location(ip_address):
    """Get location from IP address"""
    try:
        g = GeoIP2()
        location = g.city(ip_address)
        return {
            'country': location['country_name'],
            'city': location['city']
        }
    except:
        return {'country': '', 'city': ''}