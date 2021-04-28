from struct import unpack_from

from struct import unpack_from
import zlib
class Create_Polyglot(object):

    def create(self, file1, ext1, file2, ext2 , path ):
        self.file1= file1
        self.file2= file2
        self.path=path

        # input1_file = open(file1, "rb")
        # self.file1_contents = input1_file.read()
        # input1_file.close()
        #
        # input2_file = open(file2, "rb")
        # self.file2_contents = input2_file.read()
        # input2_file.close()
        #
        # if ext1 == "png" or ext1 == "jpg" or ext1 == "jpeg" :
        #     method_name = "create_image" + "_"+ ext2
        # else:
        #     method_name = "create_" + ext1 + "_" + ext2
        method_name = "create_" + ext1 + "_" + ext2
        method = getattr(self, method_name, lambda: 'Invalid File Type')
        return method()

    # def create_pdf_zip(self):
    #     new_file = open(self.path, 'wb')
    #     new_file.write(self.file1_contents)
    #     new_file.write(self.file2_contents)
    #     new_file.close()
    #     return self.path

    # def create_image_zip(self):
    #     PNG_MAGIC  = b"\x89PNG\r\n\x1a\n"
    #     png_header = self.file1.read(len(PNG_MAGIC))
    #
    #
    #     new_file = open(self.path, 'wb')
    #     new_file.write(png_header)
    #     new_file.write(self.file1_contents)
    #     new_file.write(self.file2_contents)
    #     new_file.close()
    #     return self.path

    def create_png_zip(self):
        png_in =open(self.file1, "rb")
        zip_content=open(self.file2, "rb")
        PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
        png_header = png_in .read(len(PNG_MAGIC))

        png_out = open(self.path, 'wb')
        png_out.write( png_header )

        # iterate through the chunks of the PNG file
        idat_body = b""

        while True:
            # parse a chunk
            chunk_len = int.from_bytes(png_in.read(4), "big")
            chunk_type = png_in.read(4)
            chunk_body = png_in.read(chunk_len)
            chunk_csum = int.from_bytes(png_in.read(4), "big")

            # if it's a non-essential chunk, skip over it
            if chunk_type not in [b"IHDR", b"PLTE", b"IDAT", b"IEND"]:
                print("Warning: dropping non-essential or unknown chunk:", chunk_type.decode())
                continue

            # take note of the image width and height, for future calculations
            if chunk_type == b"IHDR":
                width, height = unpack_from(">II", chunk_body)
                print(f"Image size: {width}x{height}px")

            # There might be multiple IDAT chunks, we will concatenate their contents
            # and write them into a single chunk later
            if chunk_type == b"IDAT":
                idat_body += chunk_body
                continue

            # the IEND chunk should be at the end, now is the time to write our IDAT
            # chunk, before we actually write the IEND chunk
            if chunk_type == b"IEND":
                start_offset = png_out.tell() + 8 + len(idat_body)
                print("Embedded file starts at offset", hex(start_offset))

                # concatenate our content that we want to embed
                idat_body += zip_content.read()

                if len(idat_body) > width * height:
                    exit("ERROR: Input files too big for cover image resolution.")

                # if its a zip file, fix the offsets
                if self.file2.endswith(".zip"):
                    print("Fixing up zip offsets...")
                    idat_body = bytearray(idat_body)
                    self.fixup_zip(idat_body, start_offset)

                # write the IDAT chunk
                png_out.write(len(idat_body).to_bytes(4, "big"))
                png_out.write(b"IDAT")
                png_out.write(idat_body)
                png_out.write(zlib.crc32(b"IDAT" + idat_body).to_bytes(4, "big"))

            # if we reached here, we're writing the IHDR, PLTE or IEND chunk
            png_out.write(chunk_len.to_bytes(4, "big"))
            png_out.write(chunk_type)
            png_out.write(chunk_body)
            png_out.write(chunk_csum.to_bytes(4, "big"))


            if chunk_type == b"IEND":
                # we're done!
                break

        png_in.close()
        zip_content.close()
        return self.path



    def fixup_zip(self, data, start_offset):
        # find the "end of central directory" marker
        end_central_dir_offset = data.rindex(b"PK\x05\x06")

        # find the number of central directory entries
        cdent_count = unpack_from("<H", data, end_central_dir_offset + 10)[0]

        # find the offset of the central directory entries, and fix it
        cd_range = slice(end_central_dir_offset + 16, end_central_dir_offset + 16 + 4)
        central_dir_start_offset = int.from_bytes(data[cd_range], "little")
        data[cd_range] = (central_dir_start_offset + start_offset).to_bytes(4, "little")

        # iterate over the central directory entries
        for _ in range(cdent_count):
            central_dir_start_offset = data.index(b"PK\x01\x02", central_dir_start_offset)
            # fix the offset that points to the local file header
            off_range = slice(central_dir_start_offset + 42, central_dir_start_offset + 42 + 4)
            off = int.from_bytes(data[off_range], "little")
            data[off_range] = (off + start_offset).to_bytes(4, "little")

            central_dir_start_offset += 1

