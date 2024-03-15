import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from io import BytesIO
from zipfile import ZipFile
from bs4 import BeautifulSoup

class CustomLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("VCSMP Modpack Updater")
        self.root.geometry("400x400")
        self.root.resizable(width=False, height=False)
    
        # Create a frame for better organization
        frame = ttk.Frame(root)
        frame.pack(padx=10, pady=10)
    
        # Modpack Location Entry
        modpack_label = ttk.Label(frame, text="Modpack Folder:")
        modpack_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    
        self.modpack_entry = ttk.Entry(frame, width=30)
        self.modpack_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    
        # Browse Button
        browse_button = ttk.Button(frame, text="Browse", command=self.browse_modpack)
        browse_button.grid(row=0, column=2, padx=5, pady=5)
    
        # Select Modpack Version Dropdown
        ttk.Label(frame, text="Select Modpack Version:").grid(row=1, column=0, columnspan=3)
        self.selected_file = tk.StringVar(root)
        self.dropdown = ttk.OptionMenu(frame, self.selected_file, "", ())
        self.dropdown.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    
        # Modpack Update Button
        update_button = ttk.Button(frame, text="Update Modpack", command=self.update_modpack)
        update_button.grid(row=3, column=0, columnspan=3, pady=10)
    
        # Server Stats Section
        server_stats_label = ttk.Label(root, text="Server Stats:")
        server_stats_label.pack()
    
        # Display Server Status (you can replace this with actual server status retrieval)
        server_status_label = ttk.Label(root, text="Server Status: Online")
        server_status_label.pack()
    
        # Display Player Count (you can replace this with actual player count retrieval)
        player_count_label = ttk.Label(root, text="Players Online: 5")
        player_count_label.pack()
    
        # Fetch latest zip files
        website_url = 'http://mc.mrpickle.ca/modpack'
        files = self.fetch_zip_files(website_url)
        self.update_dropdown_options(files)
    
    def browse_modpack(self):
        modpack_folder = filedialog.askdirectory(title="Select Modpack Folder")
        if modpack_folder:
            self.modpack_entry.delete(0, tk.END)
            self.modpack_entry.insert(0, modpack_folder)

    def update_modpack(self):
        modpack_folder = self.modpack_entry.get()
        selected_file = self.selected_file.get()
        if not modpack_folder:
            messagebox.showerror("Update Modpack", "Please enter or browse for a Modpack Folder.")
            return
        if not selected_file:
            messagebox.showerror("Update Modpack", "Please select a Modpack Version.")
            return

        modpack_destination = os.path.join(modpack_folder, "mods")

        try:
            # Delete existing .jar files
            for file_name in os.listdir(modpack_destination):
                if file_name.endswith(".jar"):
                    file_path = os.path.join(modpack_destination, file_name)
                    os.remove(file_path)

            # Download and extract selected zip file
            file_url = 'http://mc.mrpickle.ca/modpack/' + selected_file
            response = requests.get(file_url)
            if response.status_code == 200:
                with ZipFile(BytesIO(response.content), "r") as zip_ref:
                    zip_ref.extractall(modpack_destination)
                messagebox.showinfo("Update Modpack", "Modpack updated successfully! Please launch Minecraft.")
            else:
                messagebox.showerror("Update Modpack", f"Failed to download modpack. Status code: {response.status_code}")

        except Exception as e:
            messagebox.showerror("Update Modpack", f"An error occurred: {str(e)}")

    def fetch_zip_files(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            files = [link.get('href').split('?')[0] for link in soup.find_all('a') if link.get('href').endswith('.zip')]
            return files
        else:
            print("Failed to fetch directory listing.")
            return []

    def update_dropdown_options(self, files):
        self.dropdown["menu"].delete(0, "end")
        for file in files:
            self.dropdown["menu"].add_command(label=file, command=tk._setit(self.selected_file, file))
        print("Updated Dropdown options")
        root.after(60000, self.update_dropdown_options)


if __name__ == "__main__":
    root = tk.Tk()
    launcher = CustomLauncher(root)
    root.mainloop()
