#!/usr/bin/env python
import sys
from os import path

import django
from django.conf import global_settings as default_settings
from django.conf import settings
from django.core.management import execute_from_command_line

# Give feedback on used versions
sys.stderr.write(f"Using Python version {sys.version[:5]} from {sys.executable}\n")
sys.stderr.write(
    "Using Django version {} from {}\n".format(
        django.get_version(), path.dirname(path.abspath(django.__file__))
    )
)

if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            },
        },
        SITE_ID=1,
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.messages",
            "django.contrib.sessions",
            "django.contrib.sites",
            "crispy_forms",
            "fluent_contents",
            "fluent_contents.tests.testapp",
            "fluentcms_contactform",
        ),
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": (),
                "OPTIONS": {
                    "loaders": (
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ),
                    "context_processors": (
                        "django.template.context_processors.debug",
                        "django.template.context_processors.i18n",
                        "django.template.context_processors.media",
                        "django.template.context_processors.request",
                        "django.template.context_processors.static",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ),
                },
            },
        ],
        MIDDLEWARE=(
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
        ),
        DEFAULT_AUTO_FIELD="django.db.models.BigAutoField",
        SECRET_KEY="testtest",
        STATIC_URL="/static/",
        ROOT_URLCONF="fluentcms_contactform.tests.urls",
        TEST_RUNNER="django.test.runner.DiscoverRunner",
        # third party:
        FLUENT_CONTENTS_CACHE_OUTPUT=False,
        CRISPY_TEMPLATE_PACK="bootstrap3",
    )

DEFAULT_TEST_APPS = [
    "fluentcms_contactform",
]


def runtests():
    other_args = list(filter(lambda arg: arg.startswith("-"), sys.argv[1:]))
    test_apps = (
        list(filter(lambda arg: not arg.startswith("-"), sys.argv[1:])) or DEFAULT_TEST_APPS
    )
    argv = sys.argv[:1] + ["test", "--traceback"] + other_args + test_apps
    execute_from_command_line(argv)


if __name__ == "__main__":
    runtests()
