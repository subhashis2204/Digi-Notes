allowed_mimetypes = ['image/png', 'image/jpg', 'image/jpeg']

def file_mimetype_allowed(file):
    if file.mimetype not in allowed_mimetypes:
        return False

    return True

def get_file_extension(file):
    return file.filename.rsplit('.', 1)[1].lower()

def find_content_type(file):
    file_extension = get_file_extension(file)

    content_type = ""
    if file_extension == 'jpg' or file_extension == '.jpeg':
        content_type = "image/jpeg"
    elif file_extension == 'png':
        content_type = "image/png"
    else:
        content_type = "application/octet-stream"

    return content_type