"""
ASGI config for equipment_visualizer project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equipment_visualizer.settings')

application = get_asgi_application()
