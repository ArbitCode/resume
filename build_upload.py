import subprocess
import json
import os
import shutil

# === Configuration ===
FILE_NAME = "resume"
OUTPUT_DIR = "out"
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
    os.makedirs(".latex", exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    command = f"pdflatex -interaction=nonstopmode -output-directory=.latex {FILE_NAME}.tex >/dev/null 2>&1"
    run_command(command)

    # Move the compiled PDF to the output directory
    os.rename(f".latex/{FILE_NAME}.pdf", OUTPUT_FILE)
    run_command("rm -rf .latex")
    print(f"PDF compiled successfully: {OUTPUT_FILE}")

def upload_to_drive():
    """Uploads the compiled PDF to Google Drive."""
    print(f"Uploading {OUTPUT_FILE} to Google Drive...")
    run_command(f"rclone copy {OUTPUT_FILE} {REMOTE_FOLDER}")

def get_public_link():
    """Retrieves the public link of the uploaded file."""
    json_data = run_command(f"rclone lsjson {REMOTE_FOLDER}")
    files = json.loads(json_data)

    for file in files:
        if file["Name"] == os.path.basename(OUTPUT_FILE):
            file_id = file["ID"]
            return f"https://drive.google.com/uc?id={file_id}&export=download"

    print("Error: Could not retrieve file ID. Upload might have failed.")
    exit(1)

def update_readme(download_link):
    """Updates readme.md with the new download link."""
    with open(README_FILE, "w") as readme:
        readme.write("# Rajaram's Resume\n\n")
        readme.write("**Download Resume:**\n\n")
        readme.write(f"[Rajaram_resume.pdf]({download_link})\n")
    print(f"Updated {README_FILE} with the latest link.")

def main():
    check_dependencies()
    compile_latex()
    upload_to_drive()
    public_link = get_public_link()
    update_readme(public_link)
    print(f"Upload completed! Resume Download Link: {public_link}")

if __name__ == "__main__":
    main()

