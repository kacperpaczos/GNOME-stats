import requests
from get_repos_data import get_repos_data
from rich.console import Console
from rich.progress import Progress

console = Console()
progress = Progress(console=console)

def fetch_gitlab_repositories():
    repositories_url = []
    page = 1
    with progress:
        while True:
            console.print(f"Processing page {page}...", style="bold blue")
            response = requests.get(f"https://gitlab.gnome.org/api/v4/groups/8/projects?per_page=100&page={page}")
            if response.status_code != 200:
                console.print("Error: Failed to fetch data", style="bold red")
                break
            data = response.json()
            if not data:
                console.print("Error: No data to process", style="bold red")
                break
            for repo in data:
                url_repo = repo['http_url_to_repo']
                repositories_url.append(url_repo)
                console.print(f"Acquired link: {url_repo}", style="bold green")
            page += 1
    return repositories_url

repositories_url = fetch_gitlab_repositories()
total_repos = len(repositories_url)
current_repo = 0
get_repos_data(repositories_url, total_repos, current_repo)


