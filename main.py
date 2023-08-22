import schedule
import time
from broker import InvertirOnline
from database import Database


class Task:

    def welcome_message(self, cr=False):
        if cr:
            print('')
        print('[+] Ejecutando InvertirOnline database backup & restore...')
        
    def execute(self):
        iol = InvertirOnline()
        data = iol.portafolio()

        
        db = Database()
        db.add_dict_data(data)

        db.upload()

    def plan(self):
        schedule.every().monday.at('18:20').do(self.execute)
        schedule.every().tuesday.at('18:20').do(self.execute)
        schedule.every().wednesday.at('18:20').do(self.execute)
        schedule.every().thursday.at('18:20').do(self.execute)
        schedule.every().friday.at('18:20').do(self.execute)
        
        self.welcome_message()

        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    task = Task()
    task.plan()

if __name__ == '__main__':
    main()
