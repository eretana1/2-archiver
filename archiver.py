#! usr/bin/env python3
import os
import sys


# Check if user is entering correct amount of arguments
def check_cl_args():
    if len(sys.argv) < 2:
        print('Usage: arch <file1> <file2> <fileN> <archiver name>.arch')
        print('Usage: unarch <archiver name>.arch')
        sys.exit(1)


# Should only be used when using unarch
# Returns an int [len of content/name]
def get_name_content_len(data) -> int:
    count = 0
    while data[count] == 0:
        count += 1

    return count


# nc = Name or Content
def get_name_content(data, nc_len) -> bytearray:
    return bytearray(bytes(data[:nc_len]))


# user is trying to archive
if 'arch' in sys.argv:
    # Create archiver file:
    archiver_file = open(sys.argv[-1], 'wb')

    for filename in sys.argv[2:-1]:
        try:
            b_file = open(filename, 'rb')  # Open file to archive
            b_file_size = os.path.getsize(filename)  # Get size of file in bytes
            b_file_name = filename.encode()  # Convert name to bytes
            b_file_name_size = len(b_file_name)  # Get length of name in bytes

            # Create file contents as byte arrays
            file_content = bytearray(b_file_name_size) + bytearray(b_file_name) + bytearray(b_file_size) + bytearray(
                b_file.read())

            archiver_file.write(file_content)
            b_file.close()
            os.remove(filename)

        except FileNotFoundError:
            print('File does not exist')

    archiver_file.close()


# User is trying to un-archive
elif 'unarch' in sys.argv:
    sys.argv = sys.argv[1:]

    # open archiver file
    try:
        archiver_file = open(sys.argv[-1], 'rb')
    except FileNotFoundError:
        os.write(1, f'{sys.argv[-1]}: File was not found. Exiting...'.encode())
        sys.exit(1)

    archiver_file_data = archiver_file.read()
    while len(archiver_file_data) != 0:
        # Get the len of the name and remove from data
        name_len = get_name_content_len(archiver_file_data)
        archiver_file_data = archiver_file_data[name_len:]

        # Get the name of file and remove from data
        file_name = get_name_content(archiver_file_data, name_len)
        archiver_file_data = archiver_file_data[name_len:]

        # Get the len of the content and remove from data
        content_len = get_name_content_len(archiver_file_data)
        archiver_file_data = archiver_file_data[content_len:]

        # Get the content of the file and remove from data
        content = get_name_content(archiver_file_data, content_len)
        archiver_file_data = archiver_file_data[content_len:]

        # Create new file and write the data
        new_file = open(file_name.decode(), 'wb')
        new_file.write(content)
        new_file.close()

    # Remove archiver
    archiver_file.close()
    os.remove(sys.argv[-1])

else:
    print('Invalid command...')
