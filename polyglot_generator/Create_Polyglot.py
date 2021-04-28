class Create_Polyglot(object):

    def create(self, file1, ext1, file2, ext2 , path ):
        self.path=path
        input1_file = open(file1, "rb")
        self.file1_contents = input1_file.read()
        input1_file.close()

        input2_file = open(file2, "rb")
        self.file2_contents = input2_file.read()
        input2_file.close()

        if ext1 == "png" or ext1 == "jpg" or ext1 == "jpeg" :
            method_name = "create_image" + "_"+ ext2
        else:
            method_name = "create_" + ext1 + "_" + ext2

        method = getattr(self, method_name, lambda: 'Invalid File Type')
        return method()

    def create_pdf_zip(self):
        new_file = open(self.path, 'wb')
        new_file.write(self.file1_contents)
        new_file.write(self.file2_contents)
        new_file.close()
        return self.path

    def create_image_zip(self):
        new_file = open(self.path, 'wb')
        new_file.write(self.file1_contents)
        new_file.write(self.file2_contents)
        new_file.close()
        return self.path
