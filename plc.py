import argparse
import logging

from eventbus.eventbus import EventBus
EventBus.get()

from core.log import IndentedFormatter

if __name__ == "__main__":
    defaultFile = "Alarm_Test.L5X"
    defaultFile = "Plc_emulator.L5X"
    
    defaultPort = 4840
    defaultLog = "app.log"    

    parser = argparse.ArgumentParser(description="PLC Emulator GUI")
    parser.add_argument(
        "--file", "-f",
        type=str,
        default=defaultFile,
        help=f"Path to the L5X file (default: {defaultFile})"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=defaultPort,
        help=f"Port (default: {defaultPort})"
    )
    parser.add_argument(
        "--log", "-l",
        type=str,
        default=defaultLog,
        help=f"Logfile (default: {defaultLog})"
    )
    parser.add_argument(
        "--log-level", "-ll",
        type=str.upper,
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: WARNING)"
    )
    parser.add_argument(
        "--log-level-file", "-llf",
        type=str.upper,
        default="ERROR",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level to file (default: WARNING)"
    )
    parser.add_argument(
        "--noui",
        action="store_true",
        default=False,
        help="Run without the GUI (headless mode)"
    )

    args = parser.parse_args()

    log_level = getattr(logging, args.log_level.upper())

    '''
    DEBUG      - detailed info, for debugging
    INFO       - general runtime info
    WARNING    - something unexpected, but program still works
    ERROR      - a failure happened
    CRITICAL   - program may not continue
    '''
    logger = logging.getLogger()
    logger.setLevel(log_level)

    log_level_file = getattr(logging, args.log_level_file.upper())

    file_handler = logging.FileHandler(args.log, encoding="utf-8")
    file_handler.setLevel(log_level_file)
    file_formatter = IndentedFormatter(
            "[%(asctime)s, %(filename)s:%(lineno)s - %(funcName)s()] %(levelname)s \n"
            "%(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    if args.noui:
        import sys
        import time
        import signal
        import threading

        try:
            from core.emulator import Emulator
            
            def debug(msg:str, level=logging.INFO):
                if level != logging.NOTSET:
                    logger.log(level, msg)

            stop_event = threading.Event()
            emulator = Emulator(args.file, args.port)

            def signal_handler(sig, frame):
                if not stop_event.set():
                    stop_event.set()
                    if emulator._is_running:
                        debug("Received stop signal. Shutting down...")
                        emulator.stop()

            signal.signal(signal.SIGINT, signal_handler)
            signal.signal(signal.SIGTERM, signal_handler)
            if hasattr(signal, "SIGBREAK"):
                signal.signal(signal.SIGBREAK, signal_handler)

            emulator.start()
            
            debug("Emulator started. Waiting for stop signal...")

            while emulator.is_alive() and not stop_event.is_set():
                time.sleep(0.5)
            debug("Stopping emulator...")

            while emulator.is_alive():
                try:
                    emulator.join(timeout=5)
                except KeyboardInterrupt:
                    signal_handler(signal.SIGINT, None)
        except Exception as e:
            debug(f"Fatal error starting emulator: {e}", logging.CRITICAL)
        finally:
            debug("Shutdown complete.")
            sys.exit(1)
    else:
        from tkinter import Tk
        from gui.gui import Gui

        root = Tk()
        app = Gui(root, args.file, args.port)

        root.mainloop()