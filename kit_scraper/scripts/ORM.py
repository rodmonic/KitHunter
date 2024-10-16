
import os
import sys

import django

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kit_hunter.settings')
django.setup()


def main():

    from app.models import Kit, KitColor

    Kit.objects.all().delete()
    KitColor.objects.all().delete()


if __name__ == "__main__":
    main()