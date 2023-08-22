import schedule
import time
import broker

def welcome_message(cr=False):
    if cr:
        print('')
    print('[+] Ejecutando InvertirOnline database backup & restore...')

def task():
    broker.main()
    return welcome_message(cr=True)

def main():
    schedule.every().monday.at('18:20').do(task)
    schedule.every().tuesday.at('18:20').do(task)
    schedule.every().wednesday.at('18:20').do(task)
    schedule.every().thursday.at('18:20').do(task)
    schedule.every().friday.at('18:20').do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    welcome_message()
    main()
