import customtkinter as ctk
from tkinter import filedialog, messagebox


class DocumentView(ctk.CTk):
    """GUI built with CustomTkinter for TechDoc Transcriber."""

    def __init__(self):
        super().__init__()
        self.title("TechDoc Transcriber - BEL")
        self.geometry("600x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=0)

        self.label = ctk.CTkLabel(
            self,
            text="Convert Documents to Markdown (Offline)",
            font=("Arial", 20, "bold"),
        )
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.select_button = ctk.CTkButton(
            self,
            text="Select Document (PDF)",
            command=None,  # configured by controller
        )
        self.select_button.grid(row=1, column=0, padx=20, pady=10)

        self.rag_toggle = ctk.CTkSwitch(
            self,
            text="Enable RAG export",
            command=None,
        )
        self.rag_toggle.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.rag_toggle.select()

        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=3, column=0, padx=20, pady=5)

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.grid(
            row=4,
            column=0,
            padx=20,
            pady=(10, 5),
            sticky="nsew",
        )

        self.developer_info_label = ctk.CTkLabel(
            self,
            text="Developed By: Vishal Raj V, E218023 - T&PS/SS/NS-1",
            font=("Arial", 10),
            text_color="gray",
        )
        self.developer_info_label.grid(
            row=5, column=0, padx=20, pady=(0, 10), sticky="e"
        )

    def show_error(self, message: str):
        messagebox.showerror("Error", message)

    def update_status(self, text: str, color: str = "gray"):
        self.status_label.configure(text=text, text_color=color)

    def set_markdown_content(self, content: str):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", content)

    def is_rag_enabled(self) -> bool:
        """Return whether the RAG export toggle is on."""
        return bool(self.rag_toggle.get())
