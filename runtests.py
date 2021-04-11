#!/usr/bin/env python
import logging
import os
import sys
from os.path import abspath, dirname

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_test_utils import DefaultTestSettings

app_name = "respond_test_app"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    RESPOND_DIAGNOSIS_LABELS=dict(
        hiv="HIV", dm="Diabetes", htn="Hypertension", chol="Cholesterol"
    ),
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, "respond_test_app", "etc"),
    EDC_NAVBAR_DEFAULT="respond_model",
    EDC_BOOTSTRAP=3,
    SUBJECT_SCREENING_MODEL="respond_test_app.subjectscreening",
    SUBJECT_CONSENT_MODEL="respond_test_app.subjectconsent",
    SUBJECT_VISIT_MODEL="respond_test_app.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="respond_test_app.subjectvisitmissed",
    SUBJECT_REQUISITION_MODEL="respond_test_app.subjectrequisition",
    SUBJECT_APP_LABEL="respond_test_app",
    LIST_MODEL_APP_LABEL="respond_test_app",
    HOLIDAY_FILE=os.path.join(base_dir, app_name, "holidays.csv"),
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "multisite",
        "edc_appointment.apps.AppConfig",
        "edc_action_item.apps.AppConfig",
        "edc_consent.apps.AppConfig",
        "edc_crf.apps.AppConfig",
        "edc_lab.apps.AppConfig",
        "edc_facility.apps.AppConfig",
        "edc_metadata.apps.AppConfig",
        "edc_reference.apps.AppConfig",
        "edc_registration.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_timepoint.apps.AppConfig",
        "edc_notification.apps.AppConfig",
        "edc_visit_schedule.apps.AppConfig",
        "edc_visit_tracking.apps.AppConfig",
        "respond_test_app.apps.AppConfig",
    ],
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    # use_test_urls=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failfast = any([True for t in sys.argv if t.startswith("--failfast")])
    failures = DiscoverRunner(failfast=failfast, tags=tags).run_tests(
        [
            "respond_models.tests",
            "respond_forms.tests",
            "respond_admin.tests",
            "respond_labs.tests",
        ]
    )
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
