import os
import tkinter as tk
from tkinter import messagebox, Toplevel, simpledialog
from function import create_data, kirim_data, open_config_window, set_komputer_status, computers_status, update_status_text

root = tk.Tk()
root.title("Network Simulation")
root.geometry("600x500")

# Set new colors and font styles for a more appealing look
root.configure(bg="#34495E")

# Create a frame for the header
header_frame = tk.Frame(root, bg="#3498db")  # Blue background (#3498db is a blue color code)
header_frame.pack(fill="x", pady=10)

# Load the image for the yellow star
current_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_directory, 'star.png')

try:
    star_image = tk.PhotoImage(file=image_path)
    star_image = star_image.subsample(int(star_image.width() / 40), int(star_image.height() / 40))  # Scale to 4x4 pixels
except tk.TclError:
    messagebox.showerror("Image Error", f"Couldn't open '{image_path}'. Please check the file path.")
    star_image = tk.PhotoImage(width=1, height=1)  # Fallback if image not found

# Add the star image to the header
star_label = tk.Label(header_frame, image=star_image, bg="#3498db")  # Background matches header frame
star_label.pack(side="left", padx=10)

# Create the text label for the header
header_label = tk.Label(header_frame, text="Network Simulation", bg="#3498db", fg="white", font=("Arial", 16, "bold"))
header_label.pack(side="top", padx=40, pady=10, expand=True)  # Use 'top' and 'expand=True' to center the label


# Prevent garbage collection of the image (keeps the image visible)
star_label.image = star_image

# Menu frame (left side) with updated colors and font
menu_frame = tk.Frame(root, bg="#BDC3C7", width=100, height=300)
menu_frame.pack(side="left", fill="y")

# Menu buttons with new styling
create_button = tk.Button(menu_frame, text="Create", font=("Arial", 12, "bold"), bg="#1ABC9C", fg="white", command=lambda: open_create_form())
create_button.pack(fill="x", padx=5, pady=5)

send_button = tk.Button(menu_frame, text="Send", font=("Arial", 12, "bold"), bg="#3498DB", fg="white", command=lambda: open_send_window(output_text))
send_button.pack(fill="x", padx=5, pady=5)

config_button = tk.Button(menu_frame, text="Config", font=("Arial", 12, "bold"), bg="#E67E22", fg="white", command=lambda: open_config_window(output_text, status_text))
config_button.pack(fill="x", padx=5, pady=5)

close_button = tk.Button(menu_frame, text="Close", font=("Arial", 12, "bold"), bg="#E74C3C", fg="white", command=root.quit)
close_button.pack(fill="x", padx=5, pady=5)

# Output frame with background change
output_frame = tk.Frame(root, bg="white")
output_frame.pack(side="top", fill="x", padx=5, pady=(5, 0), expand=True)

# Output label and text area with improved color scheme
output_label = tk.Label(output_frame, text="Output", bg="#34495E", fg="white", anchor="w", font=("Arial", 10, "bold"))
output_label.pack(fill="x")
output_text = tk.Text(output_frame, height=10, bg="white", fg="black")
output_text.pack(fill="both", expand=True)

# Status frame (non-interactive)
status_frame = tk.Frame(root, bg="#BDC3C7", width=300, height=200)
status_frame.pack(side="top", fill="x", padx=5, pady=(5, 10), expand=True)

status_label = tk.Label(status_frame, text="Device Status", bg="#BDC3C7", fg="black", font=("Arial", 12, "bold"))
status_label.pack(anchor="w", padx=5, pady=5)

# Create a read-only text widget to display device statuses
status_text = tk.Text(status_frame, height=5, bg="#BDC3C7", fg="black", state=tk.DISABLED)
status_text.pack(fill="both", expand=True)

# Bottom buttons (Start, Pause, Reset)
button_frame = tk.Frame(root, bg="#34495E")
button_frame.pack(side="bottom", fill="x", pady=20)

start_button = tk.Button(button_frame, text="Start", font=("Arial", 12, "bold"), bg="#27AE60", fg="white", width=10, command=lambda: kirim_data(output_text, 'E'))
pause_button = tk.Button(button_frame, text="Pause", font=("Arial", 12, "bold"), bg="#F1C40F", fg="black", width=10)
reset_button = tk.Button(button_frame, text="Reset", font=("Arial", 12, "bold"), bg="#C0392B", fg="white", width=10, command=lambda: output_text.delete(1.0, tk.END))

# Pack buttons side by side with padding
start_button.pack(side="left", padx=20)
pause_button.pack(side="left", padx=20)
reset_button.pack(side="left", padx=20)

# Functions (unchanged)
def open_create_form():
    create_window = Toplevel(root)
    create_window.title("Create Data")
    create_window.geometry("300x250")

    # Create input fields
    name_label = tk.Label(create_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(create_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    id_label = tk.Label(create_window, text="ID:")
    id_label.grid(row=1, column=0, padx=10, pady=5)
    id_entry = tk.Entry(create_window)
    id_entry.grid(row=1, column=1, padx=10, pady=5)

    size_label = tk.Label(create_window, text="File Size:")
    size_label.grid(row=2, column=0, padx=10, pady=5)
    size_entry = tk.Entry(create_window)
    size_entry.grid(row=2, column=1, padx=10, pady=5)

    # Dropdown for file size units
    unit_label = tk.Label(create_window, text="Unit:")
    unit_label.grid(row=3, column=0, padx=10, pady=5)
    unit_var = tk.StringVar(create_window)
    unit_var.set("MB")  # default value
    unit_dropdown = tk.OptionMenu(create_window, unit_var, "Bytes", "KB", "MB", "GB", "TB")
    unit_dropdown.grid(row=3, column=1, padx=10, pady=5)

    # Function to convert file size to bytes
    def convert_to_bytes(size, unit):
        units = {'Bytes': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
        return float(size) * units[unit]

    # Function to handle data creation
    def create_data_action():
        try:
            file_size_in_bytes = convert_to_bytes(size_entry.get(), unit_var.get())
            data = {
                "name": name_entry.get(),
                "id": id_entry.get(),
                "file_size": file_size_in_bytes
            }
            create_data(output_text, data)  # Insert created data into output text
            update_status_text(status_text)  # Update status display
            create_window.destroy()  # Close window after creating data
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number for file size.")
    
    # Submit button
    submit_button = tk.Button(create_window, text="Submit", command=create_data_action)
    submit_button.grid(row=4, column=1, padx=10, pady=10)

def open_send_window(output_text):
    """ Function to open a window for sending data to a target device """
    target_device = simpledialog.askstring("Send Data", "Send to target device (A, B, C, D, E):")

    if target_device in computers_status:
        # Call the send data function with the target device
        kirim_data(output_text, target_device)
        update_status_text(status_text)  # Update status after sending data
    else:
        messagebox.showerror("Invalid Device", "Please enter a valid device (A, B, C, D, E).")

def update_status_text(status_text):
    """ Update the status text area with the current statuses of computers """
    status_text.config(state=tk.NORMAL)  # Enable editing to update
    status_text.delete(1.0, tk.END)  # Clear existing text
    for device, status in computers_status.items():
        status_text.insert(tk.END, f"{device}: {status}\n")
    status_text.config(state=tk.DISABLED)  # Disable editing again

root.mainloop()
