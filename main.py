from announcements import check_announcements
import time

def main():
    while True:
        try:
            check_announcements()
            time.sleep(2)
        except Exception as e:
            if (e == KeyboardInterrupt) :
                exit(0)
            else:
                main()      

if __name__ == '__main__':
    print("Checking annoucements...")
    main()
