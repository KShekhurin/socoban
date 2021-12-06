from app import App
from frames import BoardFrame

def main():
    frame = BoardFrame()
    application = App(frame, (600, 400))
    application.start()


if __name__ == '__main__':
    main()