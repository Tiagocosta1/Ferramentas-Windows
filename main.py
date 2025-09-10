# app.py (Corrigido e funcional)

import customtkinter as ctk

# CORREÇÃO: Importa as classes Mixin em vez das funções soltas
from app.interface import InterfaceMixin
from app.scripts import ScriptsMixin

from app.menu import (
    MenuDiagnostic,
    MenuFix,
    MenuMain,
    MenuNetwork,
    MenuOtimization,
)
from app.style import (
    BaseButton,
    MenuLabel,
    TerminalFrame,
    MenuFrame,
    TerminalOutput,
)


# CORREÇÃO: A classe principal agora herda dos Mixins, além de ctk.CTk
class WorkbenchForWindos(ctk.CTk, InterfaceMixin, ScriptsMixin):
    def __init__(self):
        super().__init__()

        self.title("Ferramentas - Windows")
        self.geometry("1000x600")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_container_frame = MenuFrame(master=self)
        self.menu_frames = {}
        self.terminal_frame = TerminalFrame(master=self)
        self.terminal_output = TerminalOutput(master=self.terminal_frame)

        self._create_all_menus()

        # CORREÇÃO: Chama as funções como métodos de 'self'
        self.start_end()
        self.show_menu("main")

    def _create_menu_generic(self, name, title, buttons_info, notMain=True):
        frame = ctk.CTkFrame(
            self.menu_container_frame, corner_radius=0, fg_color="transparent"
        )
        frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frames[name] = frame

        last_row = len(buttons_info) + 2
        frame.grid_rowconfigure(last_row, weight=1)

        MenuLabel(master=frame, text=title)

        for i, (text, command) in enumerate(buttons_info, start=1):
            BaseButton(frame, text=text, command=command, row=i)

        if notMain:
            BaseButton(
                frame,
                text="Voltar",
                command=lambda: self.show_menu(
                    "main"
                ),  # CORREÇÃO: self.show_menu
                row=last_row,
            )
        return frame

    def _create_all_menus(self):
        # Esta parte já estava correta
        butonsMainDict = MenuMain(self)
        butonsMain = list(butonsMainDict.items())
        main_frame = self._create_menu_generic(
            "main", "Menu Principal", butonsMain, notMain=False
        )
        BaseButton(
            main_frame, text="Sair", command=self.quit, row=len(butonsMain) + 2
        )

        butonsNetworkDict = MenuNetwork(self)
        buttons_network = list(butonsNetworkDict.items())
        self._create_menu_generic("network", "Rede", buttons_network)

        butonsOtimizationDict = MenuOtimization(self)
        buttons_otimization = list(butonsOtimizationDict.items())
        self._create_menu_generic(
            "otimization", "Otimização", buttons_otimization
        )

        butonsDiagnosticDict = MenuDiagnostic(self)
        buttons_diagnostic = list(butonsDiagnosticDict.items())
        self._create_menu_generic(
            "diagnostic", "Diagnóstico", buttons_diagnostic
        )

        buttonsFixDict = MenuFix(self)
        buttons_fix = list(buttonsFixDict.items())
        self._create_menu_generic("fix", "Manutenção", buttons_fix)

    def _prepare_powershell_command(self, command):
        ps_script = f"""
        $PSDefaultParameterValues['Out-File:Encoding'] = 'UTF8'
        [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
        chcp 65001 > $null
        {command}
        """
        return [
            "powershell.exe",
            "-ExecutionPolicy",
            "Bypass",
            "-NoProfile",
            "-Command",
            ps_script,
        ]

    def executar_powershell_em_thread(self, command, task_name, admin=False):
        self._mostrar_header(task_name, admin)

        def run_command():
            try:
                full_command = self._prepare_powershell_command(command)
                output, error = self._execute_subprocess(full_command)
                self._schedule_gui_updates(output, error, task_name)
            except FileNotFoundError:
                self._mostrar_erro("ERRO: O PowerShell não foi encontrado.")
            except Exception as exc:
                self._mostrar_erro(f"Ocorreu um erro inesperado: {exc}")

        self._iniciar_thread(run_command)


if __name__ == "__main__":
    app = WorkbenchForWindos()
    app.mainloop()
