import tkinter as tk
import requests
from bs4 import BeautifulSoup
import os

def fetch_zip_files(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        files = [link.get('href').split('?')[0] for link in soup.find_all('a') if link.get('href').endswith('.zip')]
        return files
    else:
        print("Failed to fetch directory listing.")
        return []

def download_selected_file(selected_file):
    if selected_file:
        # Replace 'your_website_url' with the actual URL where your .zip files are hosted
        file_url = 'http://mc.mrpickle.ca/modpack/' + selected_file
        response = requests.get(file_url)
        with open(selected_file, 'wb') as f:
            f.write(response.content)
        print(f"{selected_file} downloaded successfully.")
    else:
        print("No file selected.")

def main():
    # Replace 'your_website_url' with the actual URL where your .zip files are hosted
    website_url = 'http://mc.mrpickle.ca/modpack'
    files = fetch_zip_files(website_url)

    root = tk.Tk()
    root.title("Zip Files Dropdown")

    selected_file = tk.StringVar(root)
    dropdown = tk.OptionMenu(root, selected_file, *files)
    dropdown.pack(padx=10, pady=10)

    download_button = tk.Button(root, text="Download Selected File", command=lambda: download_selected_file(selected_file.get()))
    download_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
