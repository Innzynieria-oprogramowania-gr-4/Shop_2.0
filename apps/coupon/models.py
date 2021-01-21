from django.db import models

# model wykorzystywany do przechowywania kuponów
class Coupon(models.Model):
    # kod, który użytkownik musi wprowadzić, aby uzyskac rabat podczas zakupów
    code = models.CharField(max_length=50, unique=True)
    # wysokość rabatu
    value = models.IntegerField()
    # wartość boolowska określająca, czy dany kupon jest aktywny
    active = models.BooleanField(default=True)
    # dostępne
    num_available = models.IntegerField(default=1)
    # użyte
    num_used = models.IntegerField(default=0)

    def __str__(self):
        return self.code

    # użyteczność kuponu
    def can_use(self):
        is_active = True

        if self.active == False:
            is_active = False
        
        if self.num_used >= self.num_available and self.num_available != 0:
            is_active = False
        
        return is_active
    
    def use(self):
        self.num_used = self.num_used + 1

        if self.num_used == self.num_available:
            self.active = False
        
        self.save()