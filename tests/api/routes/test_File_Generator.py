from unittest import TestCase
from utils.testing.Direct_API_Server import Direct_API_Server

class test_File_Distributor(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Direct_API_Server().setup()
        cls.prefix = 'file-generator'

    def test_generate(self):
        path = f"{self.prefix}/generate"

        # pdf type and 2 files
        json_obj = {
            "file_type": "pdf",
            "num_of_files": 2,
        }
        response = self.client.POST(path, json=json_obj, )

        assert response ==  "2 files of type 'pdf' are generated"

    def test_generate_failure_1(self):
        path = f"{self.prefix}/generate"

        # invalid type of file
        json_obj = {
            "file_type": "xyz",
            "num_of_files": 2,
        }
        response = self.client.POST( path, json=json_obj, )

        assert response == "File Type is not supported or Invalid File Type"

    def test_generate_failure_2(self):
        path = f"{self.prefix}/generate"

        # invalid type of file
        json_obj = {
            "file_type": "pdf",
            "num_of_files": 0,
        }
        response = self.client.POST( path, json=json_obj, )

        assert response == "Number of files must be greater than 0"



