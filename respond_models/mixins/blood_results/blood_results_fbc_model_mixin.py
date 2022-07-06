from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import PROTECT
from edc_constants.choices import YES_NO
from edc_model.validators import datetime_not_future
from edc_reportable import (
    CELLS_PER_MILLIMETER_CUBED,
    CELLS_PER_MILLIMETER_CUBED_DISPLAY,
    GRAMS_PER_DECILITER,
    PERCENT,
    TEN_X_9_PER_LITER,
)
from edc_reportable.choices import REPORTABLE

from ...constants import BLOOD_RESULTS_FBC_ACTION


class BloodResultsFbcModelMixin(models.Model):
    action_name = BLOOD_RESULTS_FBC_ACTION

    tracking_identifier_prefix = "FB"

    # Full blood count ############################
    fbc_requisition = models.ForeignKey(
        settings.SUBJECT_REQUISITION_MODEL,
        on_delete=PROTECT,
        related_name="fbc",
        verbose_name="Requisition",
        null=True,
        blank=True,
        help_text="Start typing the requisition identifier or select one from this visit",
    )

    fbc_assay_datetime = models.DateTimeField(
        verbose_name="Result Report Date and Time",
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    # Hb
    haemoglobin = models.DecimalField(decimal_places=1, max_digits=6, null=True, blank=True)

    haemoglobin_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((GRAMS_PER_DECILITER, GRAMS_PER_DECILITER),),
        null=True,
        blank=True,
    )

    haemoglobin_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    haemoglobin_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # HCT
    hct = models.DecimalField(
        validators=[MinValueValidator(1.0), MaxValueValidator(999.0)],
        verbose_name="Hematocrit",
        decimal_places=2,
        max_digits=6,
        null=True,
        blank=True,
    )

    hct_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=((PERCENT, PERCENT),),
        null=True,
        blank=True,
    )

    hct_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    hct_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # RBC
    rbc = models.DecimalField(
        decimal_places=2,
        max_digits=6,
        validators=[MinValueValidator(1.0), MaxValueValidator(999999.0)],
        verbose_name="Red blood cell count",
        null=True,
        blank=True,
    )

    rbc_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),
            (CELLS_PER_MILLIMETER_CUBED, CELLS_PER_MILLIMETER_CUBED),
        ),
        null=True,
        blank=True,
    )

    rbc_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    rbc_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # WBC
    wbc = models.DecimalField(
        verbose_name="WBC", decimal_places=2, max_digits=6, null=True, blank=True
    )

    wbc_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),
            (CELLS_PER_MILLIMETER_CUBED, CELLS_PER_MILLIMETER_CUBED_DISPLAY),
        ),
        null=True,
        blank=True,
    )

    wbc_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    wbc_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    # platelets
    platelets = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)],
        null=True,
        blank=True,
    )

    platelets_units = models.CharField(
        verbose_name="units",
        max_length=15,
        choices=(
            (TEN_X_9_PER_LITER, TEN_X_9_PER_LITER),
            (CELLS_PER_MILLIMETER_CUBED, CELLS_PER_MILLIMETER_CUBED_DISPLAY),
        ),
        null=True,
        blank=True,
    )

    platelets_abnormal = models.CharField(
        verbose_name="abnormal", choices=YES_NO, max_length=25, null=True, blank=True
    )

    platelets_reportable = models.CharField(
        verbose_name="reportable",
        choices=REPORTABLE,
        max_length=25,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        verbose_name = "Blood Result: FBC"
        verbose_name_plural = "Blood Results: FBC"
