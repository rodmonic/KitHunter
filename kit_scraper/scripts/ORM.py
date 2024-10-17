
import os
import sys

import django

sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kit_hunter.settings')
django.setup()


def main():

    from app.models import Kit, KitPart, KitPartColor

    Kit.objects.all().delete()
    KitPart.objects.all().delete()
    KitPartColor.objects.all().delete()


if __name__ == "__main__":
    main()
