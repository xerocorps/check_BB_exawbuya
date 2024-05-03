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

def search_and_prompt(term, root):
    # Setting up Chrome webdriver with a specific window size
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=640,1280')
    driver = webdriver.Chrome(options=options)
    
    # Google search with the term
    driver.get(f'https://www.google.com/search?q=%22{term}%22+bug+bounty')

    # Wait until search results are loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.yuRUbf')))

    # Prompting user
    response = messagebox.askyesno("Prompt", f"Want to save this '{term}' to file?")
    
    if response:
        with open('Found_Bug_Bounty_Programs.txt', 'a') as f:
            f.write(term + '\n')

    driver.quit()

def main():
    parser = argparse.ArgumentParser(description='Search and prompt user to save terms from a file')
    parser.add_argument('-f', '--file', type=str, help='Input file containing search terms')
    args = parser.parse_args()

    if args.file:
        # Read terms from the input file
        with open(args.file, 'r') as f:
            terms = f.readlines()

        # Remove newline characters and ignore lines starting with "Bucket:"
        terms = [term.strip() for term in terms if not term.startswith("Bucket:")]

        # Create root Tkinter window
        root = tk.Tk()
        root.withdraw()

        # Bring the Tkinter window to the front periodically
        bring_to_front(root)

        # Iterate through terms and search
        for term in terms:
            search_and_prompt(term, root)
            root.update()  # Update window to remain responsive
            root.grab_set()  # Make dialog modal

        root.destroy()  # Destroy the Tkinter window after all prompts are shown
    else:
        print("Please provide an input file using the -f or --file flag.")

if __name__ == "__main__":
    main()
