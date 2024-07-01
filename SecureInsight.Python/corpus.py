import os
import asyncio
import subprocess

class Corpus:
    # Dictionary mapping programming languages to their file extensions
    LANGUAGE_TO_EXTENSION = {
        'c': '.c',
        'c++': '.cpp',
        'csharp': '.cs',
        'java': '.java',
        'python': '.py',
        'delphi': '.pas',
        'pascal': '.pas',
        'php': '.php',
        'rust': '.rs',
        'javascript': '.js',
        'typescript': '.ts',
        # Add more languages and their extensions here as needed
    }

    def __init__(self, language: str, remote_url, path, progress_callback=None, status_callback=None):
        self.language = self.LANGUAGE_TO_EXTENSION.get(language.lower(), language)
        self.remote_url = remote_url
        self.path = path
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.repo_name = os.path.splitext(os.path.basename(self.remote_url))[0].split('/')[-1] # Extract repository name
        self.processed_hashes_file = f"{self.repo_name}_processed_hashes.txt" # File to store processed commit hashes

    # Load already processed commit hashes from file
    def load_processed_hashes(self):
        try:
            with open(self.processed_hashes_file, 'r', encoding='utf-8') as file:
                return set([line.strip() for line in file.readlines()])
        except FileNotFoundError:
            return set()

    # Save new commit hashes to file
    def save_processed_hashes(self, commit_hashes):
        with open(self.processed_hashes_file, 'a', encoding='utf-8') as file:
            for commit_hash in commit_hashes:
                file.write(f"{commit_hash}\n")

    # Function to mark commit hashes as processed
    def mark_commit_processed(self, commit_hashes):
        with open(self.processed_hashes_file, 'a', encoding='utf-8') as file:
            for commit_hash in commit_hashes:
                file.write(f"{commit_hash}\n")

    # Run git command in the specified path
    def run_git_command(self, command):
        try:
            result = subprocess.run(command, cwd=self.path, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.status_callback(f"Error running git command {command}: {e}")
            return None

    # Count all commits across all branches
    def count_all_commits(self, max_count=None):
        total_commit_count = 0
        branches = self.get_all_branches() # Get all branches from remote
        self.status_callback(f"Branches found: {branches}")
        for branch in branches:
            command = f'git rev-list --count {"--max-count=" + str(max_count) if max_count else ""} {branch}'
            result = subprocess.run(command, cwd=self.path, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, result.args, result.stderr)
            branch_commit_count = int(result.stdout.strip())
            self.status_callback(f"Branch {branch} has {branch_commit_count} commits")
            total_commit_count += branch_commit_count
        return total_commit_count

    # Retrieve all remote branches
    def get_all_branches(self):
        init_output = self.run_git_command(['git', 'init']) # Initialize git repository if not already
        if init_output:
            self.status_callback(init_output)
    
        remotes = self.run_git_command(['git', 'remote']) # Get list of remotes
        if remotes and 'origin' in remotes.split('\n'):
            self.status_callback("Remote 'origin' already exists, updating it.")
            self.run_git_command(['git', 'remote', 'set-url', 'origin', self.remote_url])
        else:
            self.status_callback("Adding remote 'origin'.")
            self.run_git_command(['git', 'remote', 'add', 'origin', self.remote_url])
    
        self.run_git_command(['git', 'config', 'http.postBuffer', '524288000']) # Configure HTTP post buffer
    
        fetch_output = self.run_git_command(['git', 'fetch', '--all']) # Fetch all branches from remote
        if fetch_output is not None:
            self.status_callback("Fetched branches from remote")
            self.status_callback(fetch_output)
        else:
            self.status_callback("Failed to fetch branches from remote")
    
        branches_output = self.run_git_command(['git', 'branch', '-r']) # List remote branches
        if branches_output:
            branches = [branch.strip() for branch in branches_output.split('\n') if branch.strip().startswith('origin/')]
            self.status_callback("Remote Tracking Branches:")
            for branch in branches:
                self.status_callback(branch)
        else:
            self.status_callback("No remote tracking branches found")
            
        return branches

    # Asynchronously fetch commit hashes for a given branch
    async def fetch_commit_hashes(self, branch):
        process = await asyncio.create_subprocess_exec(
            'git', 'log', '--pretty=format:%H', branch,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            commit_hashes = stdout.decode().split('\n')
            return commit_hashes
        else:
            self.status_callback(f"Error fetching commit hashes for branch {branch}: {stderr.decode()}")
            return []
        
    # Fetch commit hashes for all branches with concurrency limit
    async def fetch_commit_hashes_with_limit(self, branches, commit_hashes, max_concurrent_tasks):
        semaphore = asyncio.Semaphore(max_concurrent_tasks)

        async def fetch_and_extend(branch):
            async with semaphore:
                hashes = await self.fetch_commit_hashes(branch)
                commit_hashes.extend(hashes)

        await asyncio.gather(*(fetch_and_extend(branch) for branch in branches))

    # Traverse all commits in all branches and process them
    def traverse_all_commits(self, output_filename: str):
        os.chdir(self.path)
        branches = self.get_all_branches()
        
        total_commits = self.count_all_commits()
        self.status_callback(f"Total commits to process: {total_commits}")
        commit_hashes = []

        asyncio.run(self.fetch_commit_hashes_with_limit(branches, commit_hashes, len(branches)))
        self.status_callback(f"Fetched {len(commit_hashes)} commit hashes.")
        asyncio.run(self.process_commits(commit_hashes, output_filename, 200, total_commits))
    
    # Asynchronously process commits
    async def process_commits(self, commit_hashes, output_filename, max_concurrent_tasks, total_commits):
        processed_hashes = self.load_processed_hashes()
        semaphore = asyncio.Semaphore(max_concurrent_tasks)
        commit_counter = 0
        source_code_buffer = ''
        commit_hashes_to_mark = []

        async def sem_process(commit_hash):
            nonlocal commit_hashes_to_mark, commit_counter, source_code_buffer
            commit_counter+=1
            self.progress_callback((commit_counter / total_commits) * 100)
            if commit_hash not in processed_hashes:
                commit_hashes_to_mark.append(commit_hash)
                if len(commit_hashes_to_mark) >= 200:
                    self.mark_commit_processed(commit_hashes_to_mark)  # Mark as processed
                    commit_hashes_to_mark = []
                async with semaphore:
                    source_code = await self.process_commit(commit_hash)
                    if source_code:
                        source_code_buffer += source_code
                        commit_counter += 1
                        if commit_counter % 100 == 0:
                            with open(output_filename, 'a', encoding='utf-8') as file:
                                file.write(source_code_buffer)
                            source_code_buffer = ''

        tasks = [sem_process(commit_hash) for commit_hash in commit_hashes]
        await asyncio.gather(*tasks)

        # Final flush for any remaining hashes
        if commit_hashes_to_mark:
            self.mark_commit_processed(commit_hashes_to_mark) 
                
        if source_code_buffer:
            with open(output_filename, 'a', encoding='utf-8') as file:
                file.write(source_code_buffer)
    
    # Process individual commit to extract source code
    async def process_commit(self, commit_hash):
        source_code = ''
        modified_files = subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit_hash], stderr=subprocess.PIPE).decode().split('\n')

        for filename in modified_files:
            if filename.endswith(self.language):
                try:
                    code = subprocess.check_output(['git', 'show', f'{commit_hash}:{filename}'], stderr=subprocess.PIPE).decode('utf-8')
                    source_code += f"\n\n{code}"
                except subprocess.CalledProcessError:
                    pass
                except UnicodeDecodeError:
                    pass
                
        return source_code     
 
    # Main function to collect commits from repositories
    def collect(self):
        try:
            total_commits_across = self.count_all_commits()
            self.status_callback(f"Total number of commits: {total_commits_across}")
            
            output_filename = f"{self.repo_name}.txt"
            self.traverse_all_commits(output_filename)
            
            return True  # Return True if everything executes without exceptions
        
        except BaseException as e:
            self.status_callback(e)
            self.status_callback("Failed to connect to Git repository")
            return True  # Return True even if there's an exception


def main():
    remote_url = 'https://github.com/mohammadalmasi/VulnerabilityDetection.git'

    path = r"C:\00\c++"
    language = 'python'
    
    # Define a progress callback
    def progress_callback(progress):
        print(f"Progress: {progress:.2f}%")

    def status_callback(status):
        print(f"status: {str(status)}")

    collector = Corpus(language, remote_url, path, progress_callback, status_callback)
    result = collector.collect()

if __name__ == "__main__":
    main()




