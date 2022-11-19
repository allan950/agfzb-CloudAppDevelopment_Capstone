from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    #def __str__(self):
    #    return "Name: {0}, Description: {1}".format(name, description)

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    type_choices = [
        ('SN', 'Sedan'), 
        ('SV', 'SUV'), 
        ('WN', 'WAGON')
    ]
    type = models.CharField(choices=type_choices, max_length=30)
    year = models.IntegerField()

    #def __str__(self):
    #    return "Make: " + self.make + ", Dealer Id: " + self.dealer_id + " Name: " + self.name + ", Type: " + self.type + ", Year: " + self.year
    

# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
