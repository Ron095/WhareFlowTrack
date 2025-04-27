from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime


# Create your models here.

class LOCMATER(models.Model):
    LOCACODE = models.CharField(max_length=4, unique=True) #Unique identifier
    LOCANAME = models.CharField(max_length=50) #Descriptive name
    LOCDESCR = models.TextField(blank=True, null=True) #Optional Description
    LOCCAPAC = models.IntegerField(validators=[MinValueValidator(0)], default=0) #Storage capacity

    def __str__(self):
        return f"{self.LOCACODE} - {self.LOCANAME} "



class INVENTPT(models.Model):
    INVENLOT = models.CharField(max_length=40, unique=True, blank=True, editable=False)
    INVENCOD = models.ForeignKey('Material_Master.MMPRODPT', on_delete=models.PROTECT)
    INVENQTY = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    INVENLOC = models.ForeignKey('LOCMATER', on_delete=models.PROTECT, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Generate custom lot number: PROD-YYYYMMDD-001
        if not self.INVENLOT:
            date_str = datetime.now().strftime('%Y%m%d')  # Format: YYYYMMDD
            product_code = self.INVENCOD # Assuming 'id' is the product identifier
            self.INVENLOT = f"PROD-{date_str}-{product_code}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.INVENCOD} (Lot: {self.INVENLOT})"


