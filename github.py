import os
from pathlib import Path
import subprocess
import requests
from dotenv import load_dotenv

load_dotenv()


class Github:
    
    database_filename = os.environ.get('DATABASE')
    db_dir = database_filename.split('/')[0] if len(database_filename.split('/')) > 1 else None
    db_name = database_filename.split('/')[-1] if len(database_filename.split('/')) > 1 else database_filename.split('/')[0]
    
    repo = os.environ.get('DATABASE_REPO')
    user, repo_name = repo.split('/')[0], repo.split('/')[1]
    github_token = os.environ.get('GITHUB_TOKEN')
    repo_url = f'https://{github_token}@github.com/{user}/{repo_name}.git'
    
    BASE_DIR = os.path.dirname(Path(__file__).resolve())
    
    def __init__(self):
        if not Path(self.db_dir).exists():
            self.clone()
        else:
            self.pull()
    
    def clone(self):
        try:
            process = subprocess.run(
                ['git', 'clone', self.repo_url, 'data'],
                cwd='.',
                stdout=subprocess.PIPE
            )
            
            if int(process.returncode) != 0:
                print('Command failed. Return code: {}'.format(process.returncode))
                raise(Exception)
        except Exception as e:
            print(e)
            
    def pull(self):
        try:
            process = subprocess.run(
                ['git', 'pull'],
                cwd=Path(self.db_dir).resolve(),
                stdout=subprocess.PIPE
            )
            
            if int(process.returncode) != 0:
                print('Command failed. Return code: {}'.format(process.returncode))
                raise(Exception)
        except Exception as e:
            print(e)

    def download(self):
        try:
            if Path(self.database_filename).exists():
                process = subprocess.run(
                    ['git', 'pull'],
                    cwd=Path(self.db_dir).resolve(),
                    stdout=subprocess.PIPE
                )
                
                if int(process.returncode) != 0:
                    print('Command failed. Return code: {}'.format(process.returncode))
                    raise(Exception)
        except Exception as e:
            print(e)

    def upload(self, message='update'):
        try:
            if Path(self.db_dir).exists():
                process = subprocess.run(
                    ['git', 'add', self.db_name],
                    cwd=Path(self.db_dir).resolve(),
                    stdout=subprocess.PIPE
                )
                
                process = subprocess.run(
                    ['git', 'commit', '-m', message],
                    cwd=Path(self.db_dir).resolve(),
                    stdout=subprocess.PIPE
                )
                
                process = subprocess.run(
                    ['git', 'push', '-u', 'origin', 'main'],
                    cwd=Path(self.db_dir).resolve(),
                    stdout=subprocess.PIPE
                )

                if int(process.returncode) != 0:
                    print('Command failed. Return code: {}'.format(process.returncode))
                    raise(Exception)
        except Exception as e:
            print(e)


def main():
    gh = Github()
    gh.upload()


if __name__ == '__main__':
    main()