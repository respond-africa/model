from django.db import models
from django.utils.html import format_html
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE
from edc_model import models as edc_models
from edc_model.models import date_not_future
from edc_model.utils import estimated_date_from_ago
from edc_visit_schedule.constants import DAY1

from ...constants import CONDITION_ABBREVIATIONS
from .clinical_review import ClinicalReviewModelMixin


class ClinicalReviewBaselineError(Exception):
    pass


class ClinicalReviewBaselineModelMixin(ClinicalReviewModelMixin):

    condition_abbrev = CONDITION_ABBREVIATIONS

    def save(self, *args, **kwargs):
        if (
            self.subject_visit.visit_code != DAY1
            and self.subject_visit.visit_code_sequence != 0
        ):
            raise ClinicalReviewBaselineError(
                f"This model is only valid at baseline. Got `{self.subject_visit}`."
            )
        for prefix in self.condition_abbrev:
            setattr(
                self,
                f"{prefix}_test_estimated_date",
                estimated_date_from_ago(self, f"{prefix}_test_ago"),
            )
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = "Clinical Review: Baseline"
        verbose_name_plural = "Clinical Review: Baseline"


class ClinicalReviewBaselineHivModelMixin(models.Model):

    hiv_test = models.CharField(
        verbose_name="Has the patient ever tested for HIV infection?",
        max_length=15,
        choices=YES_NO,
    )

    hiv_test_ago = edc_models.DurationYMDField(
        verbose_name="How long ago was the patient's most recent HIV test?",
        null=True,
        blank=True,
        help_text="If positive, most recent HIV(+) test",
    )

    hiv_test_estimated_date = models.DateField(
        null=True,
        blank=True,
        editable=False,
        help_text="calculated by the EDC using `hiv_test_ago`",
    )

    hiv_test_date = models.DateField(
        verbose_name="Date of patient's most recent HIV test?",
        validators=[edc_models.date_not_future],
        null=True,
        blank=True,
    )

    hiv_dx = models.CharField(
        verbose_name=format_html(
            "Has the patient ever tested <U>positive</U> for HIV infection?"
        ),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If yes, complete form `HIV Initial Review`",
    )

    def save(self, *args, **kwargs):
        self.hiv_test_estimated_date = estimated_date_from_ago(self, "hiv_test_ago")
        super().save(*args, **kwargs)  # type: ignore

    class Meta:
        abstract = True


class ClinicalReviewBaselineHtnModelMixin(models.Model):

    htn_test = models.CharField(
        verbose_name="Has the patient ever tested for Hypertension?",
        max_length=15,
        choices=YES_NO,
    )

    htn_test_ago = edc_models.DurationYMDField(
        verbose_name="If Yes, how long ago was the patient tested for Hypertension?",
        null=True,
        blank=True,
    )

    htn_test_estimated_date = models.DateField(
        null=True,
        blank=True,
        help_text="calculated by the EDC using `htn_test_ago`",
    )

    htn_test_date = models.DateField(
        verbose_name="Date of patient's most recent Hypertension test?",
        validators=[edc_models.date_not_future],
        null=True,
        blank=True,
    )

    htn_dx = models.CharField(
        verbose_name=format_html("Has the patient ever been diagnosed with Hypertension"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If yes, complete form `Hypertension Initial Review`",
    )

    def save(self, *args, **kwargs):
        self.htn_test_estimated_date = estimated_date_from_ago(self, "htn_test_ago")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class ClinicalReviewBaselineDmModelMixin(models.Model):

    dm_test = models.CharField(
        verbose_name="Has the patient ever tested for Diabetes?",
        max_length=15,
        choices=YES_NO,
    )

    dm_test_ago = edc_models.DurationYMDField(
        verbose_name="If Yes, how long ago was the patient tested for Diabetes?",
        null=True,
        blank=True,
    )

    dm_test_estimated_date = models.DateField(
        null=True,
        blank=True,
        help_text="calculated by the EDC using `dm_test_ago`",
    )

    dm_test_date = models.DateField(
        verbose_name="Date of patient's most recent Diabetes test?",
        validators=[edc_models.date_not_future],
        null=True,
        blank=True,
    )

    dm_dx = models.CharField(
        verbose_name=format_html("Have you ever been diagnosed with Diabetes"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If yes, complete form `Diabetes Initial Review`",
    )

    def save(self, *args, **kwargs):
        self.dm_test_estimated_date = estimated_date_from_ago(self, "dm_test_ago")
        super().save(*args, **kwargs)  # type: ignore

    class Meta:
        abstract = True


class ClinicalReviewBaselineCholModelMixin(models.Model):

    chol_test = models.CharField(
        verbose_name="Has the patient ever tested for High Cholesterol?",
        max_length=15,
        choices=YES_NO,
    )

    chol_test_ago = edc_models.DurationYMDField(
        verbose_name="If Yes, how long ago was the patient tested for High Cholesterol?",
        null=True,
        blank=True,
    )

    chol_test_estimated_date = models.DateField(
        null=True,
        blank=True,
        help_text="calculated by the EDC using `chol_test_ago`",
    )

    chol_test_date = models.DateField(
        verbose_name="Date of patient's most recent Cholesterol test?",
        validators=[date_not_future],
        null=True,
        blank=True,
    )

    chol_dx = models.CharField(
        verbose_name=format_html("Have you ever been diagnosed with High Cholesterol"),
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text="If yes, complete form `High Cholesterol Initial Review`",
    )

    def save(self, *args, **kwargs):
        self.chol_test_estimated_date = estimated_date_from_ago(self, "chol_test_ago")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
