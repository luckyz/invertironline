import schedule
import time
import broker

def task():
    return broker.main()

def main():
    schedule.every().monday.at('18:00').do(task)
    schedule.every().tuesday.at('18:00').do(task)
    schedule.every().wednesday.at('18:00').do(task)
    schedule.every().thursday.at('18:00').do(task)
    schedule.every().friday.at('18:00').do(task)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    #main()
    schedule.every().thursday.at('16:38').do(task)
    while True:
        schedule.run_pending()
        time.sleep(1)