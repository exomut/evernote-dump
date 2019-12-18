import base64  # Decodes base64
import mimetypes  # Converts mime file types into an extension
import hashlib  # Used to get md5 hash from attachments
import binascii  # Used to convert hash output to string
import os
from datetime import datetime

from utilities.tool_kit import check_for_double, make_dir_check, path_safe_string


class Attachment(object):
    """
    Attachment Class convert the base64 byte string into an actual file.
    File name extension is guessed from mime type if not found.
    """
    MEDIA_PATH = "media/"
    TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

    def __init__(self):
        self._created_date = datetime.now()
        self._filename = ""
        self._mime = ""
        self._base64data = []
        self._raw_data = b""
        self._attributes = []
        self._path = ""
        self._hash = ""
        self._uuid = ""

    def add_found_attribute(self, attr, data_line):
        self._attributes.append([attr, data_line])

    def create_file(self):
        # Create the file and set the original timestamps
        path = os.path.join(make_dir_check(os.path.join(self._path, self.MEDIA_PATH)), self._filename)
        with open(path, 'wb') as outfile:
            outfile.write(self._raw_data)
        os.utime(path, (self._created_date.timestamp(), self._created_date.timestamp()))
        self._raw_data = b""

    def create_filename(self, keep_file_names):
        base = self._filename

        if self._filename.count('.') >= 1:
            extension = self._filename.split('.')[-1]
            base = self._filename.rstrip('.' + extension)
        else:
            try:
                # Create an extension if no original filename found.
                extension = mimetypes.guess_extension(self._mime, False)[1:]
                if extension == "jpe":
                    extension = "jpg"
            except (ValueError, TypeError):
                extension = "unknown"

        if keep_file_names and base:
            # Limit filename length to 128 characters
            self._filename = path_safe_string(base[:128]) + '.' + extension
        else:
            # Create a filename from created date if none found or unwanted
            self._filename = self._created_date.strftime(self.TIME_FORMAT) + '.' + extension

        # Remove spaces from filenames since markdown links won't work with spaces
        self._filename = self._filename.replace(" ", "_")

        # Try the filename and if a file with the same name exists add a counter to the end
        self._filename = check_for_double(os.path.join(self._path, self.MEDIA_PATH), self._filename)

    def create_hash(self):
        md5 = hashlib.md5()
        md5.update(self._raw_data)
        self._hash = binascii.hexlify(md5.digest()).decode()

    def finalize(self, keep_file_names):
        try:
            self.create_filename(keep_file_names)
        except NameError:
            self.create_filename(True)
        self.decode_base64()
        self.create_hash()
        self.create_file()

    def get_attributes(self):
        # Create a string of markdown code neatly formatted for all attributes
        export = "\n[%s](%s%s)" % (self._filename, self.MEDIA_PATH, self._filename)
        if len(self._attributes) > 0:
            export += "\n>hash: %s  " % self._hash
            for attr in self._attributes:
                export += "\n>%s: %s  " % (attr[0], attr[1])
            export += "\n"
        return export

    def get_extension(self, mime_type):
        if self._filename.count('.') >= 1:
            return '.' + self._filename.split('.')[-1]
        else:
            extension = mimetypes.guess_extension(mime_type)
            return extension.replace('.jpe', '.jpg')

    def get_filename(self):
        return self._filename

    def get_hash(self):
        return self._hash

    def get_uuid(self):
        return self._uuid

    def data_stream_in(self, data_line):
        self._base64data.append(data_line.rstrip('\n'))

    def decode_base64(self):
        # Decode base64 image to memory
        try:
            self._raw_data = base64.b64decode(''.join(self._base64data))
            self._base64data = []
        except TypeError:
            raise SystemExit

    def set_created_date(self, created_date):
        self._created_date = created_date

    def set_filename(self, filename):
        self._filename = filename

    def set_mime(self, mime):
        self._mime = mime

    def set_path(self, path):
        self._path = path

    def set_uuid(self, uuid):
        self._uuid = uuid
