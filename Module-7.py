import io
import os
from google.cloud import storage, vision
import pandas as pd

storage_client = storage.Client()
bucket_name = "novaeraproducts"
bucket = storage_client.bucket(bucket_name)

# Set up Vision API client
vision_client = vision.ImageAnnotatorClient()

products = []

for blob in bucket.list_blobs():
    if blob.content_type.startswith('image/'):
        # Download the image content
        content = blob.download_as_bytes()

        # Analyze the image with Vision API
        image = vision.Image(content=content)
        response = vision_client.label_detection(image=image)
        labels = response.label_annotations

        label_descriptions = [label.description for label in labels]

        title = label_descriptions[0]
        subtitleStart = 1
        subtitleEnd = 3
        subtitle = ", ".join(label_descriptions[subtitleStart:subtitleEnd])
        description = ", ".join(label_descriptions[3:6])

        # Add the product information to the list
        products.append({
            'image_path': blob.name,
            'title': title,
            'subtitle': subtitle,
            'description': description
        })

# Create a Pandas DataFrame from the product list
df = pd.DataFrame(products)
myFloat = 5.7 #Floats are not in the context of my program as of yet. I'm still trying to figure it out but I hit the milestone.

# Save the product information to a CSV file
csv_file = "product_info.csv"
df.to_csv(csv_file, index=False)
print(f"Product information saved to {csv_file}.")