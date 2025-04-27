from django.core.management.base import BaseCommand
import threading
from Material_Master.models import MMPRODPT


class Command(BaseCommand):
    help = "Simulate concurrent creation of products"

    def handle(self, *args, **kwargs):
        # Function to create a product

        def create_product():
            product = MMPRODPT()
            product.save()
            print(f"Product created with code: {product.MMPROCDE}")

        # Number of threads (simulating concurrent requests)
        number_of_threads = 10

        # Create threads
        threads = []
        for _ in range(number_of_threads):
            t = threading.Thread(target=create_product)  # Each thread creates a product
            threads.append(t)

        # Start threads
        for t in threads:
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        # Verify results
        products = MMPRODPT.objects.values_list('MMPROCDE', flat=True)
        print(f"Generated product codes: {products}")
        print(f"Unique codes: {len(set(products))}, Total codes: {len(products)}")
