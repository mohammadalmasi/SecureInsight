import os

class FileSplitter:
    def __init__(self, input_file, parts=2):
        self.input_file = input_file
        self.parts = parts
        self.base_name, self.extension = os.path.splitext(input_file)
    
    def split_file(self):
        try:
            # First, determine the total number of lines in the file
            with open(self.input_file, 'r', encoding='utf-8', errors='replace') as infile:
                total_lines = sum(1 for line in infile)

            lines_per_part = total_lines // self.parts

            with open(self.input_file, 'r', encoding='utf-8', errors='replace') as infile:
                for i in range(self.parts):
                    output_file = f"{self.base_name}_part{i+1}{self.extension}"
                    with open(output_file, 'w', encoding='utf-8', errors='replace') as outfile:
                        start_index = i * lines_per_part
                        end_index = (i + 1) * lines_per_part if i < self.parts - 1 else total_lines

                        for _ in range(start_index, end_index):
                            line = infile.readline()
                            if line:
                                outfile.write(line)
                            else:
                                break

                    print(f"Part {i+1} written to '{output_file}'.")

        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = r'C:\00\test\corpus.txt'  # Use raw string to avoid escape sequence issues
    splitter = FileSplitter(input_file, parts=10)
    splitter.split_file()
 # C:\00\test\corpus_part4.txt