import gzip

def compress_file(input_file, output_file):
    with open(input_file, 'rb') as f_in:
        with gzip.open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)

def decompress_file(input_file, output_file):
    with gzip.open(input_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            f_out.writelines(f_in)

# Example usage:
input_file = 'example.txt'
compressed_file = 'example.txt.gz'
decompressed_file = 'example_decompressed.txt'

# Compress the file
compress_file(input_file, compressed_file)
print(f"{input_file} compressed to {compressed_file}")

# Decompress the file
decompress_file(compressed_file, decompressed_file)
print(f"{compressed_file} decompressed to {decompressed_file}")
