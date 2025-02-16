import subprocess
import json
import os
import shutil

# === Configuration ===
FILE_NAME = "Rajaram_resume"
OUTPUT_DIR = ".latex"
OUTPUT_FILE = f"{OUTPUT_DIR}/Rajaram_resume.pdf"
REMOTE_FOLDER = "GDRIVE:resume"
README_FILE = "README.md"

def run_command(command):
    """Runs a shell command and returns output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}\n{e.stderr}")
        exit(1)

def check_dependencies():
    """Checks if required commands exist."""
    for cmd in ["pdflatex", "rclone", "jq"]:
        if not shutil.which(cmd):
            print(f"Error: {cmd} is not installed.")
            exit(1)

def compile_latex():
    """Compiles the LaTeX file into a PDF."""
    print("Compiling LaTeX file...")
    os.makedirs(f"{OUTPUT_DIR}", exist_ok=True)
    
    command = f"pdflatex -interaction=nonstopmode -output-directory={OUTPUT_DIR} {FILE_NAME}.tex >/dev/null 2>&1"
    run_command(command)

    print(f"PDF compiled successfully: {OUTPUT_FILE}")

def upload_to_drive():
    """Uploads the compiled PDF to Google Drive."""
    print(f"Uploading {OUTPUT_FILE} to Google Drive...")
    run_command(f"rclone copy {OUTPUT_FILE} {REMOTE_FOLDER}")
    run_command(f"rm -rf {OUTPUT_DIR}")

def update_readme():
    """Updates readme.md with the new download link."""
    public_link = run_command(f"rclone link {REMOTE_FOLDER}/{FILE_NAME}.pdf")
    print(f"Upload completed! Resume Download Link: {public_link}")
    with open(README_FILE, "w") as readme:
        readme.write("# Rajaram's Resume\n\n")
        readme.write("**Download Resume:**\n\n")
        readme.write(f"[Rajaram_resume.pdf]({public_link})\n")
    print(f"Updated {README_FILE} with the latest link.")

def main():
    check_dependencies()
    compile_latex()
    upload_to_drive()
    update_readme()

if __name__ == "__main__":
    main()

