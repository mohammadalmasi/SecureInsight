import requests
import zipfile
import os
from pathlib import Path
from urllib.parse import urlparse
import uuid

class GitZipDownloader:
    def __init__(self, zip_url, extract_dir):
        """
        Initialize the GitZipDownloader with the URL of the zip file and the directory to extract files to.
        """
        self.zip_url = zip_url
        self.extract_dir = extract_dir

    def download_zip(self):
        """
        Download the zip file from the specified URL and save it to the extraction directory.
        Generates a unique name for the zip file to avoid conflicts.
        Returns the path to the downloaded zip file.
        """
        response = requests.get(self.zip_url)
        response.raise_for_status()

        zip_name = os.path.basename(urlparse(self.zip_url).path)
        unique_zip_name = f"{uuid.uuid4()}_{zip_name}"
        zip_path = os.path.join(self.extract_dir, unique_zip_name)
        
        with open(zip_path, "wb") as f:
            f.write(response.content)
        
        print(f"Downloaded zip file to {zip_path}")
        return zip_path

    def extract_zip(self, zip_path):
        """
        Extract the contents of the specified zip file to the extraction directory.
        Ensures all directories and files are created properly.
        """
        os.makedirs(self.extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            for member in zip_ref.infolist():
                member_path = Path(self.extract_dir) / member.filename

                try:
                    if member.is_dir():
                        # Create directories if the member is a directory
                        member_path.mkdir(parents=True, exist_ok=True)
                    else:
                        # Create parent directories if the member is a file
                        member_path.parent.mkdir(parents=True, exist_ok=True)
                        # Extract file contents
                        with zip_ref.open(member) as source, open(member_path, "wb") as target:
                            target.write(source.read())
                except Exception as e:
                    print(f"Failed to extract {member.filename}: {e}")

        print(f"Extracted files to {self.extract_dir}")

    def download_and_extract(self):
        """
        Download and extract the zip file. Returns the path of the first extracted folder, if any.
        """
        zip_path = self.download_zip()
        self.extract_zip(zip_path)
    
        extracted_items = os.listdir(self.extract_dir)
        extracted_folders = [item for item in extracted_items if os.path.isdir(os.path.join(self.extract_dir, item))]
        extracted_folders_full_paths = [os.path.join(self.extract_dir, folder) for folder in extracted_folders]
    
        print(f"Extracted files and directories: {extracted_folders_full_paths}")
    
        if extracted_folders_full_paths:
            first_extracted_folder = extracted_folders_full_paths[0]
            print(f"First extracted folder: {first_extracted_folder}")
        else:
            first_extracted_folder = None
            print("No folders found in the extracted directory.")
            
        return first_extracted_folder

if __name__ == "__main__":
    extract_dir = r"C:\Workloads\SecureInsight\SecureInsight.Python\git_zip_downloade"
    zip_urls=[
        "https://github.com/dotnet/runtime/archive/refs/heads/main.zip",
        "https://github.com/dotnet/roslyn/archive/refs/heads/main.zip",
        "https://github.com/dotnet/aspnetcore/archive/refs/heads/main.zip",
        "https://github.com/dotnet/winforms/archive/refs/heads/main.zip",
        "https://github.com/dotnet/aspire/archive/refs/heads/main.zip",
        "https://github.com/dotnet/arcade-services/archive/refs/heads/main.zip",
    ]
    
    for zip_url in zip_urls:
        downloader = GitZipDownloader(zip_url, extract_dir)
        extracted_folder = downloader.download_and_extract()
    
    print(extracted_folder)
