import os, shutil

def delete_unnecessary_data(output_folder):
    # remove the media folder inside the output folder
    media_folder = os.path.join(output_folder, "media")
    if os.path.exists(media_folder):
        shutil.rmtree(media_folder)