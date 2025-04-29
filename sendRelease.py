import os
import sys
import argparse
from github import Github

def create_github_release(token, repo_name, tag_name, release_name, body, files):
    """
    Create a GitHub release and upload specified files
    
    Args:
        token (str): GitHub personal access token
        repo_name (str): Repository name in format "username/repo"
        tag_name (str): Tag name for the release (e.g., "v1.0.0")
        release_name (str): Name of the release (e.g., "Version 1.0.0")
        body (str): Description/release notes
        files (list): List of file paths to upload
    """
    try:
        # Initialize GitHub API
        g = Github(token)
        repo = g.get_repo(repo_name)
        
        print(f"Creating release {release_name} on {repo_name}...")
        
        # Create the release
        release = repo.create_git_release(
            tag=tag_name,
            name=release_name,
            message=body,
            draft=False,
            prerelease=False
        )
        
        # Upload each file
        for file_path in files:
            if os.path.exists(file_path):
                print(f"Uploading {file_path}...")
                release.upload_asset(file_path)
                print(f"Successfully uploaded {file_path}")
            else:
                print(f"Warning: File {file_path} not found, skipping.")
        
        print(f"Release created successfully: {release.html_url}")
        return True
    
    except Exception as e:
        print(f"Error creating release: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Create a GitHub release and upload files")
    parser.add_argument("--token", required=True, help="GitHub personal access token")
    parser.add_argument("--repo", required=True, help="Repository name (username/repo)")
    parser.add_argument("--tag", required=True, help="Tag name for the release (e.g., v1.0.0)")
    parser.add_argument("--name", required=True, help="Release name")
    parser.add_argument("--body", default="New release", help="Release description/notes")
    parser.add_argument("--files", nargs="+", required=True, help="Files to upload")
    
    args = parser.parse_args()
    
    success = create_github_release(
        args.token,
        args.repo,
        args.tag,
        args.name,
        args.body,
        args.files
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()