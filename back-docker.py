import subprocess
import tarfile
import os
import datetime
import glob

def stop_all_docker_containers():
    try:
        subprocess.run("docker stop $(docker ps -q)", check=True, shell=True)
        print("All Docker containers stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping Docker containers: {e}")

def start_all_docker_containers():
    try:
        subprocess.run("docker start $(docker ps -a -q)", check=True, shell=True)
        print("All Docker containers started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error starting Docker containers: {e}")

# ... rest of the file remains unchanged ...

def add_directory_to_archive(directory_path, archive_name, destination_path):
    try:
        archive_full_path = os.path.join(destination_path, archive_name)
        with tarfile.open(archive_full_path, "w:gz") as tar:
            tar.add(directory_path, arcname=os.path.basename(directory_path))
        print(f"Directory {directory_path} added to archive {archive_full_path} successfully.")
    except Exception as e:
        print(f"Error adding directory to archive: {e}")

def cleanup_old_archives(destination_path):
    try:
        archives = sorted(glob.glob(os.path.join(destination_path, "*.tar.gz")), key=os.path.getmtime)
        now = datetime.datetime.now()
        keep = set()

        for archive in archives:
            archive_time = datetime.datetime.fromtimestamp(os.path.getmtime(archive))
            age_days = (now - archive_time).days

            if age_days == 0:
                keep.add(archive)
            elif age_days == 7:
                keep.add(archive)
            elif age_days == 30:
                keep.add(archive)

        for archive in archives:
            if archive not in keep:
                os.remove(archive)
                print(f"Removed old archive: {archive}")
    except Exception as e:
        print(f"Error cleaning up old archives: {e}")

if __name__ == "__main__":
    directory_to_archive = "/home/triiq/docker"
    destination_path = "/home/triiq/backups"
    
    # Generate archive name based on the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    archive_name = f"backup_{current_date}.tar.gz"

    stop_all_docker_containers()
    add_directory_to_archive(directory_to_archive, archive_name, destination_path)
    start_all_docker_containers()
    cleanup_old_archives(destination_path)
