import os
import json
import django
from django.contrib.auth.hashers import make_password
from django.conf import settings
from dotenv import load_dotenv


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ingenium.settings')
django.setup()

load_dotenv()


if __name__ == '__main__': 
    admin_username = os.getenv('ADMIN_USERNAME')
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')

    hashed_password = make_password(admin_password)

    fixture = [
        {
            "model": "users.user",
            "pk": 2,
            "fields": {
                "password": hashed_password,
                "last_login": None,
                "is_superuser": True,
                "username": admin_username,
                "first_name": "admin",
                "last_name": "",
                "email": admin_email,
                "is_staff": True,
                "is_active": True,
                "date_joined": "2024-08-09T15:29:34.524Z",
                "groups": [],
                "user_permissions": []
            }
        }
    ]

    output_path = 'users/fixtures/user.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(fixture, f, indent=4)

