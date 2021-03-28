from django.core.exceptions import ImproperlyConfigured
from edc_constants.constants import DM, YES
from edc_form_validators import FormValidator

from respond_model.utils.form_utils import raise_if_initial_review_does_not_exist

from ..form_validators_mixins import CrfFormValidatorMixin, GlucoseFormValidatorMixin
from ..utils import raise_if_baseline, raise_if_clinical_review_does_not_exist


class GlucoseFormValidator(
    GlucoseFormValidatorMixin,
    CrfFormValidatorMixin,
    FormValidator,
):

    required_if_baseline = True
    require_diagnosis = False

    def clean(self):

        if self.cleaned_data.get("subject_visit"):
            if not self.required_if_baseline:
                raise_if_baseline(self.cleaned_data.get("subject_visit"))
            raise_if_clinical_review_does_not_exist(self.cleaned_data.get("subject_visit"))
            if self.require_diagnosis:
                raise_if_initial_review_does_not_exist(
                    self.cleaned_data.get("subject_visit"), DM
                )
            if "glucose_performed" not in self.cleaned_data:
                raise ImproperlyConfigured("Missing field. Expected 'glucose_performed'")
            self.validate_glucose_test()