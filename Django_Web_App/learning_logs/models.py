from django.db import models

class Topic(models.Model):
    #Define the topic the user is learning about
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        #return a string rep of the model
        return self.text
