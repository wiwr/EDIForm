import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.messagebox as messagebox
import json

class FormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EDI Form")

        self.form_data = {
            "customer_name": "",
            "customer_id": "",
            "message_type": "",
            "message_format": "",
            "communication_protocol": "",
            "additional_fields": {}
        }

        self.createForm()


    def createForm(self):
        # First Column
        first_column = tk.Frame(self.root)
        first_column.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Customer Name
        tk.Label(first_column, text="Customer Name:").grid(row=0, column=0)
        self.customer_name_entry = tk.Entry(first_column)
        self.customer_name_entry.grid(row=0, column=1)

        # Customer ID
        tk.Label(first_column, text="Customer ID:").grid(row=1, column=0)
        self.customer_id_entry = tk.Entry(first_column)
        self.customer_id_entry.grid(row=1, column=1)

        # Message Type
        tk.Label(first_column, text="Message Type:").grid(row=2, column=0)
        self.message_type_entry = tk.Entry(first_column)
        self.message_type_entry.grid(row=2, column=1)

        # Message Format
        tk.Label(first_column, text="Message Format:").grid(row=3, column=0)
        self.message_format_entry = tk.Entry(first_column)
        self.message_format_entry.grid(row=3, column=1)

        # Second Column
        second_column = tk.Frame(self.root)
        second_column.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Communication Protocol
        tk.Label(second_column, text="Communication Protocol:").grid(row=0, column=0, sticky="w")
        self.communication_protocol_var = tk.StringVar()
        self.communication_protocol_dropdown = ttk.Combobox(second_column, textvariable=self.communication_protocol_var)
        self.communication_protocol_dropdown['values'] = ("SFTP client", "SFTP server", "FTP client", "FTP server", "AS2")
        self.communication_protocol_dropdown.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.communication_protocol_dropdown.bind("<<ComboboxSelected>>", self.onProtocolSelected)

        # Additional Fields
        self.additional_fields = {}
        self.additional_fields["host_label"] = tk.Label(second_column, text="Host:")
        self.additional_fields["host_entry"] = tk.Entry(second_column)
        self.additional_fields["user_label"] = tk.Label(second_column, text="User:")
        self.additional_fields["user_entry"] = tk.Entry(second_column)
        self.additional_fields["password_label"] = tk.Label(second_column, text="Password:")
        self.additional_fields["password_entry"] = tk.Entry(second_column, show="*")
        self.additional_fields["key_label"] = tk.Label(second_column, text="Key File:")
        self.additional_fields["key_entry"] = tk.Entry(second_column, state="disabled")
        self.additional_fields["key_browse_button"] = tk.Button(second_column, text="Browse", command=self.browseKeyFile)

        for field in self.additional_fields.values():
            field.grid_forget()

        # Submit Button
        tk.Button(self.root, text="Submit", command=self.submitForm).grid(row=1, columnspan=2, pady=10)

        # Disable resizing of the window
        self.root.resizable(False, False)


    def onProtocolSelected(self, event):
        selected_protocol = self.communication_protocol_var.get()

        for field in self.additional_fields.values():
            field.grid_forget()

        if selected_protocol == "AS2":
            self.additional_fields["sender_id_label"] = tk.Label(self.additional_fields["host_label"].master, text="Sender ID:")
            self.additional_fields["sender_id_entry"] = tk.Entry(self.additional_fields["host_entry"].master)
            self.additional_fields["dest_id_label"] = tk.Label(self.additional_fields["host_label"].master, text="Destination ID:")
            self.additional_fields["dest_id_entry"] = tk.Entry(self.additional_fields["host_entry"].master)
            self.additional_fields["host_label"].grid(row=2, column=0, sticky="w")
            self.additional_fields["host_entry"].grid(row=2, column=1)
            self.additional_fields["sender_id_label"].grid(row=3, column=0, sticky="w")
            self.additional_fields["sender_id_entry"].grid(row=3, column=1)
            self.additional_fields["dest_id_label"].grid(row=4, column=0, sticky="w")
            self.additional_fields["dest_id_entry"].grid(row=4, column=1)

        elif selected_protocol == "SFTP client":
            self.additional_fields["host_label"].grid(row=2, column=0, sticky="w")
            self.additional_fields["host_entry"].grid(row=2, column=1)
            self.additional_fields["user_label"].grid(row=3, column=0, sticky="w")
            self.additional_fields["user_entry"].grid(row=3, column=1)
            self.additional_fields["password_label"].grid(row=4, column=0, sticky="w")
            self.additional_fields["password_entry"].grid(row=4, column=1)

        elif selected_protocol == "SFTP server":
            self.additional_fields["host_label"].grid(row=2, column=0, sticky="w")
            self.additional_fields["host_entry"].grid(row=2, column=1)
            self.additional_fields["user_label"].grid(row=3, column=0, sticky="w")
            self.additional_fields["user_entry"].grid(row=3, column=1)
            self.additional_fields["password_label"].grid(row=4, column=0, sticky="w")
            self.additional_fields["password_entry"].grid(row=4, column=1)
            self.additional_fields["key_label"].grid(row=5, column=0, sticky="w")
            self.additional_fields["key_entry"].grid(row=5, column=1, sticky="ew")
            self.additional_fields["key_browse_button"].grid(row=5, column=2)


    def browseKeyFile(self):
        file_path = filedialog.askopenfilename(filetypes=[("Key files", "*.key")])
        self.additional_fields["key_entry"].config(state="normal")
        self.additional_fields["key_entry"].delete(0, tk.END)
        self.additional_fields["key_entry"].insert(0, file_path)
        self.additional_fields["key_entry"].config(state="disabled")


    def submitForm(self):
        # Get values from entry fields
        customer_name = self.customer_name_entry.get()
        customer_id = self.customer_id_entry.get()
        message_type = self.message_type_entry.get()
        message_format = self.message_format_entry.get()
        communication_protocol = self.communication_protocol_var.get()

        # Check if all required fields are filled
        if not all([customer_name, customer_id, message_type, message_format, communication_protocol]):
            messagebox.showerror("Error", "Please fill in all required fields.")           
            return

        # Get values from additional fields
        additional_fields_data = {}
        for key, entry in self.additional_fields.items():
            # Ensure to only retrieve values from Entry widgets
            if isinstance(entry, tk.Entry):
                value = entry.get()
                if value:
                    additional_fields_data[key] = value

        # Check if key content needs to be fetched
        if "key_entry" in additional_fields_data:
            key_file_path = additional_fields_data["key_entry"]
            if key_file_path:
                with open(key_file_path, "r") as key_file:
                    key_content = key_file.read()
                    additional_fields_data["key_content"] = key_content

        # Update form data
        self.form_data["customer_name"] = customer_name
        self.form_data["customer_id"] = customer_id
        self.form_data["message_type"] = message_type
        self.form_data["message_format"] = message_format
        self.form_data["communication_protocol"] = communication_protocol
        self.form_data["additional_fields"] = additional_fields_data

        # Dump form data into JSON file
        with open("form_data.json", "w") as file:
            json.dump(self.form_data, file)

        print("Form data saved as JSON.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormApp(root)
    root.mainloop()

