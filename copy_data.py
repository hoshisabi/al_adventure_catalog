import os
import shutil

source_file = r'f:\Users\decha\Documents\Projects\al_adventure_catalog\_data\all_adventures.json'
destination_dir = r'f:\Users\decha\Documents\Projects\al_adventure_catalog\_site\data'
destination_file = os.path.join(destination_dir, 'all_adventures.json')

# Create the destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Copy the file
shutil.copy(source_file, destination_file)

print(f"Successfully copied {source_file} to {destination_file}")