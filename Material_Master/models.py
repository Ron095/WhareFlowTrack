from django.db import models, transaction, IntegrityError

# Create your models here.

#MATERIAL MASTER TABLE
class MMPRODPT(models.Model):
    MMPROCDE = models.CharField(max_length=14, unique=True, editable=False)
    MMPRODES = models.CharField(max_length=40)
    MMPROPRE = models.CharField(max_length=10)
    MMPROSTA = models.BooleanField(default=True)
    MMPRODAT = models.DateTimeField(auto_now_add=True)

    BASE_NUMBER = 14000000000001 # Set your base number

    # Advantages of This Implementation
    # Atomic: Prevents race conditions using database-level locks (select_for_update).
    # Safe: Ensures uniqueness via the unique=True constraint at the database level.
    # Scalable: Handles high-concurrency scenarios gracefully with retries and locking.
    # Efficient: Generates sequential product codes dynamically without needing separate #counters or unnecessary dependency tables.

    def generate_unique_code(self):
        with transaction.atomic():   #Ensure atomic block (prevents race conditions) Lock rows to prevent concurrent updates
            last_product = MMPRODPT.objects.select_for_update().order_by('-MMPROCDE').first()
            if not last_product:
                # If no products exist, start with BASE_NUMBER
                return str(self.BASE_NUMBER)

            # Increment the last code and return it
            last_code = int(last_product.MMPROCDE)
            new_code = last_code + 1
            return str(new_code)

    # here we are modifying Django "save method" and creating a unique code and handle Unique Constraint Violations Gracefully
    def save(self, *args, **kwargs):
        if not self.MMPROCDE:
            retries = 3 #Retry mechanism for unique constraint violations, Define retry attempts for rare collisions
            for attempt in range(retries):
                self.MMPROCDE = self.generate_unique_code()
                try:
                    super().save(*args, **kwargs) #Attempt saving
                    break #Exit loop if save succeeds
                except IntegrityError:
                    if attempt == retries - 1:  #On the final attempt, raise the error
                        raise IntegrityError("Failed to generate a unique product code after multiple attempts") # Retry (generate a new code)


    def __str__(self):
        return self.MMPROCDE
