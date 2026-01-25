#!/bin/bash

# Navigate to the directory containing your zip files if necessary
# cd /path/to/your/zip/files/

# Loop through all files ending with .zip (case-insensitive)
for archive in *.[Zz][Ii][Pp]; do
    # Check if a file actually matches the pattern to prevent issues if no files exist
    if [[ -e "$archive" ]]; then
        # Extract the filename without the extension
        # ${archive%.*} removes the shortest match of .* from the end of the filename
        dir_name="${archive%.*}"
        
        # Create the directory
        mkdir -p "$dir_name"
        
        # Unzip the archive into the newly created directory
        unzip "$archive" -d "$dir_name"
    fi
done
