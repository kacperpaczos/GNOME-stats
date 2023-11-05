import json
import git
from git import Repo
import os
import shutil
import datetime
from rich.progress import track
from rich.console import Console
from repo_stats import repo_stats
from repo_stats import error_log

console = Console()
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

def download_data(repo_urls, total_repos, current_repo):
    all_commits = []
    for repo_url in track(repo_urls, description="Downloading..."):
        console.print(f"Repository: {repo_url.split('/')[-1]}", style="bold blue")
        repo_name = repo_url.split('/')[-1]
        commits = repo_stats(repo_url, total_repos, current_repo)
        if commits is not False:
            all_commits.append((commits, repo_name))
    return all_commits

def save_data(all_commits):
    for commits, repo_name in track(all_commits, description="Saving...     "):
        if commits is False or commits is None or len(commits) == 0:
            console.print("Error: No data to save or an error occurred", style="bold red")
            with open(error_log, 'a') as f:
                f.write(f"Error: No data to save or an error occurred for {repo_name}\n")
        else:
            with open(os.path.join(data_dir, f"{repo_name}_commits_data.json"), 'a') as f:
                for commit in commits:
                    json.dump(commit, f)
                console.print(f"Data has been saved, file location: {os.path.join(data_dir, f'{repo_name}_commits.json')}", style="bold green")

def get_repos_data(repo_urls, total_repos, current_repo):
    for repo_url in repo_urls:
        commits = download_data([repo_url], total_repos, current_repo)
        save_data(commits)
