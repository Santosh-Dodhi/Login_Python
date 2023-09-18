from django.db import models

# Create your models here.


# Creating Tables

class user_record(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    # def __str__(self):
    #     return self.user_id


class searched_product(models.Model):
    product_id = models.CharField(max_length=50 , primary_key=True)
    # user_id = models.ForeignKey(user_record, on_delete=models.CASCADE)
    frequency = models.IntegerField()


class company(models.Model):
    company_id = models.IntegerField()
    company_name = models.CharField(max_length=50) 
    def __str__(self):
        return self.company_id


class product_price_history(models.Model):
    product_id = models.CharField(max_length=50 , primary_key=True)
    price = models.BigIntegerField()
    company_id = models.ForeignKey(company , on_delete=models.CASCADE)