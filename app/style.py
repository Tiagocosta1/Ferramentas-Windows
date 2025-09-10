# style.py (Corrigido)

import customtkinter as ctk


class BaseButton(ctk.CTkButton):
    def __init__(self, master, text, command, row, sticky="ew", **kwargs):
        super().__init__(master=master, text=text, command=command, **kwargs)
        self.grid(row=row, column=0, padx=25, pady=5, sticky=sticky)


class TerminalFrame(ctk.CTkFrame):
    # CORREÇÃO: Adicionado o parâmetro 'master' que estava faltando.
    def __init__(self, master, **kwargs):
        super().__init__(
            master=master, corner_radius=0, fg_color="black", **kwargs
        )
        self.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class MenuFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, width=250, corner_radius=0, **kwargs)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class TerminalOutput(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        super().__init__(
            master=master,
            wrap="word",
            font=("Consolas", 12),
            text_color="white",
            activate_scrollbars=True,
            fg_color="black",
            border_color="gray",
            border_width=1,
            scrollbar_button_color="gray",
            scrollbar_button_hover_color="darkgray",
        )
        self.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.configure(state="disabled")


class MenuLabel(ctk.CTkLabel):
    def __init__(self, master, text, **kwargs):
        super().__init__(
            master=master,
            text=text,
            font=ctk.CTkFont(size=18, weight="bold"),
            **kwargs
        )
        self.grid(row=0, column=0, padx=20, pady=(20, 10))
