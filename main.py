import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, source_folder, dest_folders):
        self.source_folder = source_folder
        self.dest_folders = dest_folders

    def on_modified(self, event):
        if not event.is_directory:
            for file in os.listdir(self.source_folder):
                src = os.path.join(self.source_folder, file)

                # Add your logic here for different file types
                if file.endswith(".pdf"):
                    dest_folder = self.dest_folders.get("pdf")
                elif file.endswith((".png", ".jpg", ".jpeg")):
                    dest_folder = self.dest_folders.get("images")
                # ... add more conditions as needed

                if dest_folder:
                    dest = os.path.join(dest_folder, file)
                    shutil.move(src, dest)


if __name__ == "__main__":
    # Change to your Downloads directory path
    path_to_watch = os.path.expanduser("~/Downloads")
    dest_folders = {
        "pdf": os.path.expanduser("~/Documents/PDFs"),
        "images": os.path.expanduser("~/Pictures"),
        # ... add more destination folders
    }

    # Check if the destination directories exist, if not, create them
    for key, folder in dest_folders.items():
        if not os.path.exists(folder):
            os.makedirs(folder)

    event_handler = DownloadHandler(path_to_watch, dest_folders)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
