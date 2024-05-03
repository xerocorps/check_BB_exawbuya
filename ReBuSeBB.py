import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import messagebox

def bring_to_front(root):
    root.attributes('-topmost', True)
    root.update_idletasks()  # Update window to ensure it's brought to front
    root.attributes('-topmost', False)
    root.after(100, lambda: bring_to_front(root))

def search_and_prompt(bucket, domain, root):
    # Setting up Chrome webdriver with a specific window size
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=640,1280')
    driver = webdriver.Chrome(options=options)
    
    # Google search with the term
    driver.get(f'https://www.google.com/search?q=%22{domain}%22+bug+bounty')

    # Wait until search results are loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.yuRUbf')))

    # Prompting user
    response = messagebox.askyesno("Prompt", f"Found bucket '{bucket}' for domain '{domain}'. Want to save this to file?")
    
    if response:
        with open('Found_Bug_Bounty_Programs.txt', 'a') as f:
            f.write(f"Bucket: {bucket}\n")
            f.write(f"Domain: {domain}\n\n")

    driver.quit()

def main():
    parser = argparse.ArgumentParser(description='Search and prompt user to save terms from a file')
    parser.add_argument('-f', '--file', type=str, help='Input file containing bucket and domain information')
    args = parser.parse_args()

    if args.file:
        # Read terms from the input file
        with open(args.file, 'r') as f:
            lines = f.readlines()

        # Prepare buckets and domains
        buckets = []
        domains = []
        current_bucket = None
        for line in lines:
            if line.startswith("Bucket:"):
                current_bucket = line.strip().split(": ")[1]
            else:
                buckets.append(current_bucket)
                domains.append(line.strip())

        # Create root Tkinter window
        root = tk.Tk()
        root.withdraw()

        # Bring the Tkinter window to the front periodically
        bring_to_front(root)

        # Iterate through buckets and domains and search
        for bucket, domain in zip(buckets, domains):
            search_and_prompt(bucket, domain, root)
            root.update()  # Update window to remain responsive
            root.grab_set()  # Make dialog modal

        root.destroy()  # Destroy the Tkinter window after all prompts are shown
    else:
        print("Please provide an input file using the -f or --file flag.")

if __name__ == "__main__":
    main()
