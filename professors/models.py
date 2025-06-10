from django.db import models

# Create your models here.
class Professor(models.Model):
    name = models.CharField(max_length = 100, unique=True)

    def __str__(self):
        return self.name 
    
class Rating(models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    teaching = models.PositiveSmallIntegerField()
    evaluation = models.PositiveSmallIntegerField()
    behaviour = models.PositiveSmallIntegerField()
    internals = models.PositiveSmallIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    