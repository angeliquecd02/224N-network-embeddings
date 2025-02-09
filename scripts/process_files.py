import zstandard
import os
import json

fields_to_keep = ["title", "id","author","selftext","subreddit","author_created_utc"]

def decompress_zst(input_file, output_file):
    """Decompresses a .zst file.

    Args:
        input_file (str): Path to the input .zst file.
        output_file (str): Path to the output file.
    """
    try:
        with open(input_file, 'rb') as compressed_file, open(output_file, 'wb') as outfile:
            decompressor = zstandard.ZstdDecompressor()
            with decompressor.stream_reader(compressed_file) as reader:
                while chunk := reader.read(16384):  # Read in chunks
                    outfile.write(chunk)
        print(f"Decompressed: {input_file} → {output_file}")

    except FileNotFoundError:
         print(f"Error: Input file '{input_file}' not found.")
    except zstandard.ZstdError as e:
        print(f"Zstandard decompression error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def process_all(in_dir, int_dir, json_dir, out_dir):
    for filename in os.listdir(in_dir):
        f = os.path.join(in_dir, filename)
        fout =os.path.join(int_dir, filename)
        f_json = os.path.join(json_dir, filename)
        f_final = os.path.join(out_dir, filename)
        decompress_zst(f, fout)
        text_to_json(fout, f_json)
        filter_json(f_json,f_final)

def text_to_json(input_file, output_file):
    data = []
    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            try:
                data.append(json.loads(line.strip()))  # Convert each line to a JSON object
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON line: {line.strip()}")

    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4)

    print(f"Converted '{input_file}' to '{output_file}'")

def filter_json(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        data = json.load(infile)  # Load JSON data

    # If it's a list of objects, filter each one
    if isinstance(data, list):
        #todo: filter out empty posts, deleted posts
        filtered_data = [{k: v for k, v in item.items() if k in fields_to_keep} for item in data]
    else:  # If it's a single object
        filtered_data = {k: v for k, v in data.items() if k in fields_to_keep}

    with open(output_file, "w", encoding="utf-8") as outfile:
        json.dump(filtered_data, outfile, indent=4)

    print(f"Filtered JSON saved to '{output_file}'")

# Example usage

def main():
    process_all("../raw_data/sample_1/raw", "../raw_data/sample_1/unzipped","../raw_data/sample_1/all_json", "../raw_data/sample_1/filtered_data")

if __name__ == "__main__":
    main()