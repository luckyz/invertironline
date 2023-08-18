import os
from pathlib import Path
import subprocess
import requests

class Github:
    def __init__(self):
        pass
        
    def download_from_github(self):
        try:
            '''process = subprocess.Popen(
                ['git', 'pull'],
                stdout=subprocess.PIPE
            )
            output = process.communicate[0]
            
            output = process.communicate[0]
            
            if int(process.returncode) != 0:
                print('Command failed. Return code : {}'.format(process.returncode))
                exit(1)
            return output'''
            os.system('git pull')
        except Exception as e:
            print(e)
            exit(1)

    def upload_to_github(self, database='db.sqlite3', message='update'):
        try:
            '''process = subprocess.run(
                ['git', 'add', database],
                cwd='.',
                stdout=subprocess.PIPE
            )
            # output = process.communicate[0]
            
            process = subprocess.run(
                ['git', 'commit', '-m', message],
                cwd='.',
                stdout=subprocess.PIPE
            )
            # output = process.communicate[0]'''
            
            if not os.exists(database):
                os.system(f'git add {database}')
                os.system(f'git commit -m "{message}"')
                os.system('git push')
            
            '''if int(process.returncode) != 0:
                print('Command failed. Return code: {}'.format(process.returncode))
                print(process.stdout)
                exit(1)
            # return output'''
        except Exception as e:
            print(e)
            #print(process.stdout)
            exit(1)
            
    def get_token():
        token = os.environ.get('GITHUB_TOKEN')
        headers = {'Authorization': 'token ' + token}

        user_login = requests.get('https://api.github.com/user', headers=headers)
        print(user_login.json())


def main():
    gh = Github()
    gh.upload_to_github()


if __name__ == '__main__':
    main()