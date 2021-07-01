from edc_reportable.grading_data.daids_july_2017 import chemistries, dummies, hematology
from edc_reportable.normal_data.africa import normal_data

grading_data = {}
grading_data.update(**dummies)
grading_data.update(**chemistries)
grading_data.update(**hematology)
