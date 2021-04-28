import zipfile

from config.Config import Config

from polyglot_generator.Create_Polyglot import Create_Polyglot
from file_generator.Create import Create
from os import path
import random
import uuid
from osbot_utils.utils.Files import temp_folder,create_folder,file_create
import ntpath
class Polyglot_Generator:

    def __init__(self):
        self.config = Config()

        self.supported_types_1 = ["png"]
        self.supported_types_2 = ["zip"]

        self.temp_folder=temp_folder()
        self.file_creator=Create()
        self.polyglot_creator = Create_Polyglot()
        self.target_folder = path.join(self.config.file_generator_location, "polyglot_files")


    def populate_polyglot(self,ext1, ext2, num_of_files):
        if num_of_files == 0:
            return -1
        if not self.validate_extension( ext1, ext2):
            return 0
        for i in range(num_of_files):
            if ext1 in self.supported_types_1:
                file1=self.populate_file1(ext1)
                file2=self.populate_file2(ext2)
                response=self.create_polyglot_file(file1, ext1, file2, ext2)
                print(response)

            else:
                file1=self.populate_file1(ext2)
                file2=self.populate_file2(ext1)
                response=self.create_polyglot_file(file1, ext2, file2, ext1)
                print(response)

        return 1

    def create_polyglot_file(self, file1, ext1, file2, ext2):
        create_folder(path.join(self.target_folder,ext1))
        self.target_path = path.join(self.target_folder,ext1, ntpath.basename(file1))
        response=self.polyglot_creator.create(file1, ext1,file2, ext2, self.target_path)
        return response

    def validate_extension(self,ext1,ext2):
        if ext1 in self.supported_types_1:
            if ext2 in self.supported_types_2:
                return True
        elif ext2 in self.supported_types_1:
            if ext1 in self.supported_types_2:
                return True

        return False

    def populate_file1(self,ext):
        unique_value = uuid.uuid4()
        path = self.temp_folder + unique_value.hex + "." + ext
        content = (str(unique_value) + "\n") * random.randint(1, 100000)
        self.file_creator.create(path, ext, content)
        return path


    def populate_file2(self,ext):
        file_creator = Create()
        unique_value = uuid.uuid4()

        content = (str(unique_value) + "\n") * random.randint(1, 100000)

        ext=random.choice(self.supported_types_1)
        ext="pdf"
        path = self.temp_folder + unique_value.hex + "."+ ext
        file_creator.create(path, ext, content)

        zip_path = self.temp_folder + unique_value.hex + ".zip"

        zipfile.ZipFile(zip_path, mode='w',compression=zipfile.ZIP_DEFLATED).write(path, unique_value.hex +"." + ext)
        return zip_path
