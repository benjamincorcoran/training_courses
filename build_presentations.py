#!usr/bin/python
#Filename: build_presentations.py 

# Build presentations from ipynb files and embed images so that the presentation
# html can be shared freely. 

import os 
import re
import pathlib
import argparse
import base64
import nbconvert



def list_presentation_files(folder='.', notebook=''):
    '''
    Return a list of all .ipynb notebooks in a given folder
    exclude checkpoints.

    Args:
        folder (str): The folder path to look for notebooks. 
                      Defaults to current working directory.

    Returns:
        list: A list of notebook paths. 
    '''
    
    # Create the folder path as a Pathlib object     
    folder_path = pathlib.Path(folder)
    
    # Add star to notebook variable if it is not blank 
    # to allow for globbing by specific string
    if notebook != '':
        notebook+='*'
    
    # Recusively search for any ipynb notebooks within the folder.     
    ipynb_files = folder_path.rglob(f'*{notebook}.ipynb')
    
    # For the notebooks found, remove any that are in a subfolder .ipynb_checkpoints
    ipynb_files = [p for p in ipynb_files if not re.findall('.ipynb_checkpoints', str(p))]  
    
    # Return the list of notebooks.
    return ipynb_files



def read_images_from_notebook(ipynb_file):
    '''
    Look for images in the notebook, extract the path to the image 
    
    Args:
        ipynb_file (pathlib.Path): The path to the notebook file 
    
    Returns:
        str: The contents of the the notebook file
        dict: A dictionary mapping the image reference in the notebook
              to the resolved path of the image
        pathlib.Path: The folder containing the notebook. 
    '''
    
    # Resolve the full path to the notebook, and get the parent folder 
    folder = ipynb_file.resolve().parents[0]
    
    # Open the ipynb_file and read the contents into notebook as a string
    with open(ipynb_file, 'r') as f:
        notebook = f.read()
    
    # Find all the <img> tags within the notebook and extract the source field 
    imgs = re.findall('<img.*?src=(.*?)(?:\s|>)', notebook)
    
    # Create a dictionary to store the image reference and resolved path. 
    img_dict = dict()
    
    # Loop over all the discovered images
    for img in imgs:
        
        try:
        # Clean up the image path, removing escape characters
            img_path_clean = re.findall(r'[\'"](.*?)[\\]*[\'"]', img)[0]
        except:
            continue
        
        # If the image is not already converted to base64
        if not re.match('data:image/', img_path_clean): 
            
            # Create the path object
            img_path = pathlib.Path(img_path_clean)

            # If the src tag in the <img> is relative add on the 
            # folder file path. 
            if img_path_clean[0] == '.':
                img_path = folder / img_path

            # Add to dictionary mapping the contents of src to the 
            # resolved file path. 
            img_dict[img] = img_path
    
    # Return the notebook contents, image look up and path to parent folder
    return notebook, img_dict, folder



def convert_image_to_base64_encode(image_path):
    '''
    Read an image from file and conver to a base64 encoded string
    
    Args:
        image_path (pathlib.Path): The filepath to an image
    
    Returns:
        str: The base64 encoded string that can be used to replace the src 
             in the notebook, embedding the image permanently. 
    '''
    
    
    # Extract the file type from the image path 
    extention = image_path.suffix[1:]
    
    # Open the image as a binary file, read into image_raw
    with open(image_path, 'rb') as f:
        image_raw = f.read()
    
    # Encode the raw binary in to base64
    b64_image = base64.b64encode(image_raw)
    
    # Convert the encoded data into a string and wrap in html to allow 
    # a web browser to interpret the data as an image. 
    str_b64_image = f'\\"data:image/{extention};base64,'+str(b64_image)[2:-1]+'\\"'
    
    # Return the encoded string representation of the image
    return str_b64_image



if __name__ == "__main__":
    
    # Add argument --find to allow for processing just one notebook
    # based on a string in the notebooks path
    parser = argparse.ArgumentParser(description='Convert .ipynb notebook into slides')
    parser.add_argument('--find', 
                        default='',
                        help='Specify a specific notebook to convert by keyword')
    
    # Parse arguments entered in the command line.
    args = parser.parse_args()
    
    # Print a header
    print('\nConverting .ipynb to slides...\n')
    
    # Get a list of presentation files in the folder
    ipynbs = list_presentation_files(notebook=args.find)
    
    # For each presentation in the the list of presentations
    for i, presentation_path in enumerate(ipynbs):
        
        # Log current presentation
        print(f'{presentation_path} ({i+1}/{len(ipynbs)})')
        
        # Read in the notebook and extract all the images
        presentation, images, folder = read_images_from_notebook(presentation_path)
        
        # Loop over the images found in the notebook
        for ref, path in images.items():
            try:
                # For each image; convert the image to a base64 string 
                encoded_image = convert_image_to_base64_encode(path)
                # Replace the original src with the base64 encoding
                presentation = presentation.replace(ref, encoded_image)
            except:
                pass

        # Create a temporary location for a copy of the notebook
        temp_presentation_path = f'{folder}/'+presentation_path.stem+'.nb'
        
        # Write the new notebook with the base64 encoded images
        with open(temp_presentation_path, 'w') as f:
            f.write(presentation)
        
        # Remove the exported slides if the file already exists
        try:
            os.unlink(presentation_path.with_suffix('.slides.html'))
        except OSError:
            pass
        
        # Run jupyter nbconvert on the temporary file, convert it to slides 
        ret = os.system(f'jupyter nbconvert "{temp_presentation_path}" --to slides --no-input 2> /dev/null')
        
        # If there is an error, log it here
        if ret != 0:
            print(f'Unable to convert {presentation_path} to slides.')
        
        # Remove the temporary notebook. 
        os.unlink(temp_presentation_path)

        
        
        
    
