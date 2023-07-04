import tkinter as tk
import socket
import subprocess
from tkinter import messagebox
import psutil

class App:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("IPv4 Address Changer")
        self.adapters = self.get_adapters()
        self.current_ip_label = tk.Label(self.master, text=self.get_current_ip())
        self.current_ip_label.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.master, text="New IPv4 Address:").grid(row=1, column=0, padx=5, pady=5)
        self.new_ip_entry = tk.Entry(self.master)
        self.new_ip_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(self.master, text="Network Adapter:").grid(row=2, column=0, padx=5, pady=5)

        # Create dropdown menu for network adapters
        self.adapter_var = tk.StringVar(value=self.adapters[0])
        self.adapter_menu = tk.OptionMenu(self.master, self.adapter_var, *self.adapters)
        self.adapter_menu.grid(row=2, column=1, padx=5, pady=5)

        # Create confirm button
        tk.Button(self.master, text="Confirm", command=self.change_ip_address).grid(row=3, column=1, padx=5, pady=5)

    def get_adapters(self):
        # Use subprocess to get list of network adapters
        output = subprocess.check_output(["netsh", "interface", "show", "interface"], universal_newlines=True)
        lines = output.split("\n")
        adapters = []
        for line in lines:
            if "Connected" in line:
                adapter = line.split()[3]
                adapters.append(adapter)
        return adapters

    def get_current_ip(self):
        addrs = psutil.net_if_addrs()
        for _, net_if_addrs in addrs.items():
            for addr in net_if_addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                    return addr.address
        return None

    def change_ip_address(self):
        # Get new IPv4 address and adapter name from widgets
        new_ip = str(self.new_ip_entry.get())
        adapter_name = self.adapter_var.get()

        # Formulate command to change IP address and execute it
        command = f"netsh interface ipv4 set address name=\"{adapter_name}\" static {new_ip} 255.255.255.0"
        subprocess.check_output(command, shell=True)

        # Show success message and update current IP address label
        new_ip_address = self.get_current_ip()
        self.current_ip_label.config(text=new_ip_address)
        messagebox.showinfo("Success!", f"IPv4 address changed to {new_ip_address}.")

if __name__ == "__main__":
    app = App()
    app.master.mainloop()