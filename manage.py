"""Manager for executing django."""

import os
import os.path
import sys


if __name__ == "__main__":
    if os.path.isfile(os.path.join(os.getcwd(), 'etc', 'local.py')) is True:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etc.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etc.production")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
