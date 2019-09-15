import os


def zipdir(path, ziph):
    """
    Create a zip directory and compress the file
    https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    """

    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
