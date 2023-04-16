import tkinter as tk
import subprocess
from requests import get
import time
from tkinter import messagebox, font
import pyglet, os
from urllib.request import urlopen
import requests
import myip
import re
import webbrowser

pyglet.font.add_file('f.ttf')
url = "https://t.me/v2hub_xyz"

class ProxyApp:
    def tg_link(self):
        webbrowser.open_new_tab(url)
    def ipn(self):
        ip = requests.get('https://api.ipgeolocation.io/getip').text
        ipv4 = re.sub(r"[^\d\.]", "", ip)
        if self.connected == True and self.process == None:
            return f"\n\nGermany\n5.75.205.133"
        else:
            return f"\n\nIran\n{ipv4}"
    def set_ip(self):
        self.ip_label.config(text=self.ipn())
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("V2hub")
        self.connected = False
        self.process = None
    	#ip = f'{requests.get('https://api.ipify.org').text}'

        # Set window dimensions and position
        self.window_width = 300
        self.window_height = 350
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (self.window_width/2))
        y_cordinate = int((screen_height/2) - (self.window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_cordinate, y_cordinate))

        # Set window background color
        self.root.configure(bg="#F0F0F0")

        # V2hub label
        self.v2hub_label = tk.Label(self.root,text="V2HUB",fg='#5DBB63',bg='#F0F0F0',font=('f',40))
        self.v2hub_label.pack()

        # Create frame for buttons and terminal
        self.frame = tk.Frame(self.root,bg='#F0F0F0')
        self.frame.pack(pady=10)


        # Add Connect/Disconnect button
        self.connect_button = tk.Button(self.frame,fg='#FFFFFF', bg='#696969',text="Connect", command=self.toggle_connection, width=10, font=("Helvetica", 12, "bold"))
        self.connect_button.pack(side=tk.LEFT)

        # Add Terminal button
        self.terminal_button = tk.Button(self.frame,fg='#FFFFFF', bg='#696969',text="Terminal", command=self.open_terminal, width=10, font=("Helvetica", 12, "bold"))
        self.terminal_button.pack(side=tk.LEFT, padx=10)

        self.ipf = tk.Frame(self.root,bg='#F0F0F0',width=129,height=129,borderwidth=10)
        self.ipf.pack(pady=10)

        # Refresh button
        #self.refresh_button = tk.Button(self.root,fg='#FFFFFF', bg='#696969',text="Refresh", command=self.set_ip, width=10, font=("Helvetica", 12, "bold"))
        #self.refresh_button.pack()

        #self.ip1_label = tk.Label(self.ipf, text=f"\n\nLocation\nIPv4", font=("Helvetica", 11),bg='#F0F0F0',fg='#555555')
        #self.ip1_label.pack(side=tk.LEFT)

        # Create label to show public IP address
        #self.ip_label = tk.Label(self.ipf,text=self.ipn(),font=("Helvetica", 12),bg='#F0F0F0')
        #self.ip_label.pack(side=tk.LEFT)


        self.logo_img = tk.PhotoImage(file="tg.png")
        self.footer = tk.Frame(self.root,bg='#F0F0F0')
        self.footer.pack(pady=10)
        self.tg_btn = tk.Button(self.footer,text='t.me/v2hub_xyz',compound="left",bg='#F0F0F0',borderwidth=0,
            image=self.logo_img, bd=0, font=("Helvetica", 13)
            ,command=self.tg_link)
        self.tg_btn.pack(side=tk.TOP)
        # developer tag
        self.developer_tag = tk.Label(self.footer,fg='#000',bg='#F0F0F0', text="\nDeveloped by GNS Rfan", font=("Helvetica", 10))
        self.developer_tag.pack(side=tk.BOTTOM)


        # Initialize terminal window
        self.terminal_window = None
    



    def toggle_connection(self):
        if not self.connected:
            # Connect
            self.connected = True

            # Set proxy settings
            subprocess.run(["netsh", "winhttp", "set", "proxy", "127.0.0.1:1080"], capture_output=True)

            # Run v2ray in a new terminal window
            self.process = subprocess.Popen(["cmd.exe", "/c", "v2ray.exe run"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 

            tk.messagebox.showinfo(title="Connected!", message="Your IP is secured by V2hub\n5.75.205.133 Germany")
            
        else:
            # Disconnect
            self.connected = False

            # Reset proxy settings
            subprocess.run(["netsh", "winhttp", "reset", "proxy"], capture_output=True)

            # Close v2ray process
            subprocess.run(["taskkill", "/f", "/im", "v2ray.exe"], capture_output=True)

            tk.messagebox.showinfo(title="Disconnected!", message="Your IP is not secured anymore")

    def open_terminal(self):
        if not self.terminal_window:
            # Create new terminal window
            self.terminal_window = tk.Toplevel()
            self.terminal_window.title("Terminal")

            # Add text widget for displaying output
            self.output_text = tk.Text(self.terminal_window)
            self.output_text.pack(expand=True, fill=tk.BOTH)

            # Add entry widget for input
            self.input_entry = tk.Entry(self.terminal_window)
            self.input_entry.pack(side=tk.BOTTOM, fill=tk.X)

            # Bind Return key to execute command
            self.input_entry.bind("<Return>", self.execute_command)

            # Focus on input entry widget
            self.input_entry.focus()

        # Minimize or deiconify terminal window
        if self.terminal_window.state() == "iconic":
            self.terminal_window.deiconify()
        else:
            self.terminal_window.iconify()

    def execute_command(self, event):
        # Get input command from entry widget
        command = self.input_entry.get().strip()

        if not command:
            # If empty command, do nothing
            return

        # Enable text widget and insert command
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"$ {command}\n")

        # Execute command in a subprocess
        try:
            process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Insert output into text widget
            self.output_text.insert(tk.END, process.stdout)
            self.output_text.insert(tk.END, process.stderr)

        except subprocess.CalledProcessError as e:
            # If command fails, insert error message
            self.output_text.insert(tk.END, f"Error: {e}\n")

        # Disable text widget and clear entry widget
        self.output_text.config(state=tk.DISABLED)
        self.input_entry.delete(0, tk.END)


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ProxyApp()
    app.run()
