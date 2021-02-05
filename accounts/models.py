from django.db import models

# Create your models here.
from django.db import models

class AD_User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    start_case_number = models.IntegerField()
    end_case_number = models.IntegerField()
    prediction_output_file = models.FileField(upload_to="data_pool")
    data_input_file = models.FileField(upload_to="data_pool")
    


    def __str__(self):
            return self.username
class AD_Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    recommendation_file = models.FileField(upload_to="data_pool")
    feedback_iframe_code = models.TextField()
    prediction_1_dropdown = models.FileField(upload_to="data_pool")
    prediction_2_dropdown = models.FileField(upload_to="data_pool")
    prediction_3_dropdown = models.FileField(upload_to="data_pool")
    recommendation_1_dropdown = models.FileField(upload_to="data_pool")
    recommendation_2_dropdown = models.FileField(upload_to="data_pool")
    recommendation_3_dropdown = models.FileField(upload_to="data_pool")




 


   
