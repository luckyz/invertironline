import schedule
import time
from broker import InvertirOnline
from database import Database


class Plan:

    def welcome_message(self, cr=False):
        if cr:
            print('')
        print('[+] Ejecutando InvertirOnline database backup & restore...')
        
    def task(self):
        iol = InvertirOnline()
        data = iol.portafolio()

        
        db = Database()
        db.add_dict_data(data)

        db.upload()

    def setup(self):
        schedule.every().monday.at('18:20').do(self.task)
        schedule.every().tuesday.at('18:20').do(self.task)
        schedule.every().wednesday.at('18:20').do(self.task)
        schedule.every().thursday.at('18:20').do(self.task)
        schedule.every().friday.at('18:20').do(self.task)
        
        self.welcome_message()

        while True:
            schedule.run_pending()
            time.sleep(1)


def main():
    plan = Plan()
    plan.setup()

if __name__ == '__main__':
    main()
