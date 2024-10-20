import tkinter as tk

# Simulated statuses for computers A, B, C, D, and E
computers_status = {
    'A': 'Koneksi Tidak Rusak',
    'B': 'Koneksi Tidak Rusak',
    'C': 'Koneksi Tidak Rusak',
    'D': 'Koneksi Tidak Rusak',
    'E': 'Koneksi Tidak Rusak',
}

def create_data(output_text, data):
    """ Create data entry and display in the output """
    output_text.insert(tk.END, f"Data Created - Name: {data['name']}, ID: {data['id']}, File Size: {data['file_size']} bytes\n")

def set_komputer_status(komputer, status):
    """ Set the connection status of a computer """
    computers_status[komputer] = status

def cek_koneksi(komputer):
    """ Check the connection status of a specific computer """
    return computers_status[komputer] == "Koneksi Tidak Rusak"

def kirim_data(output_text, target_device):
    """ Send data to the target device through the network """
    devices_chain = ['A', 'B', 'C', 'D', 'E']

    # Find the index of the target_device in the chain
    if target_device not in devices_chain:
        output_text.insert(tk.END, f"Invalid target device: {target_device}.\n")
        return

    # Start sending process
    output_text.insert(tk.END, f"Memulai pengiriman data ke {target_device}...\n")
    
    # Check the status of each device in the chain up to the target_device
    for device in devices_chain[:devices_chain.index(target_device) + 1]:
        output_text.insert(tk.END, f"Mengirim data ke perangkat {device}...\n")
        if not cek_koneksi(device):
            output_text.insert(tk.END, f"Pengiriman gagal. Koneksi pada perangkat {device} Rusak.\n")
            return
        output_text.insert(tk.END, f"Data berhasil diterima oleh perangkat {device}.\n")

    # If all devices are functional, confirm data sending
    output_text.insert(tk.END, f"Data berhasil dikirim ke perangkat {target_device}.\n")

def open_config_window(output_text, status_text):
    """ Function to open the configuration window and allow changing of computer statuses """
    config_window = tk.Toplevel()
    config_window.title("Configuration")
    config_window.geometry("400x300")

    # List of computers to update status
    computers = ['A', 'B', 'C', 'D', 'E']
    status_var = {komp: tk.StringVar(value=computers_status[komp]) for komp in computers}

    def update_status():
        for komp in computers:
            set_komputer_status(komp, status_var[komp].get())
        update_status_text(status_text)  # Update status display after changing statuses
        config_window.destroy()  # Close the configuration window

    for idx, komp in enumerate(computers):
        tk.Label(config_window, text=f"Status Komputer {komp}:").grid(row=idx, column=0, padx=10, pady=5)
        tk.OptionMenu(config_window, status_var[komp], "Koneksi Tidak Rusak", "Koneksi Rusak").grid(row=idx, column=1, padx=10, pady=5)

    # Update button
    update_button = tk.Button(config_window, text="Update Status", command=update_status)
    update_button.grid(row=len(computers), column=1, pady=10)

def update_status_text(status_text):
    """ Update the status text area with the current statuses of computers """
    status_text.config(state=tk.NORMAL)  # Enable editing to update
    status_text.delete(1.0, tk.END)  # Clear previous status
    for komp, status in computers_status.items():
        status_text.insert(tk.END, f"Status Komputer {komp}: {status}\n")  # Add each computer's status
    status_text.config(state=tk.DISABLED)  # Disable editing to make it read-only
