import os
from werkzeug.utils import secure_filename

class UploadService:
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions

    def allowed_file(self, fname):
        return '.' in fname and fname.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.upload_folder, filename))
            return True, filename
        return False, None
