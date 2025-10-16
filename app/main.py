import customtkinter as ctk
from interface import InterfaceMixin
from scripts import ScriptsMixin
from menu import (
    MenuMain,
    MenuInfoDiag,
    MenuRelatory,
    MenuShowLogs,
    MenuShowLists,
    MenuManutOtim,
    MenuCleanArchives,
    MenuOtimDisk,
    MenuFixSistem,
    MenuCheckIntegrity,
    MenuRepairComponents,
    MenuRestorePoints,
    MenuNetwork,
    MenuNetworkDiag,
    MenuNetworkFix,
    MenuNetworkConfig,
    MenuFirewall,
    MenuSecurity,
    MenuAdminSystem,
    MenuAdminTools,
    MenuUserManagement,
    MenuInterfaceSettings,
    MenuGeneralSettings,
    MenuSoftApp,
    MenuInstallPrograms,
)
from style import (
    BaseButton,
    MenuLabel,
    TerminalFrame,
    MenuFrame,
    TerminalOutput,
)


class WorkbenchForWindows(ctk.CTk, InterfaceMixin, ScriptsMixin):
    def __init__(self):
        super().__init__()
        self.title("Ferramentas - Windows")
        self.geometry("1200x700")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.menu_container_frame = MenuFrame(master=self)
        self.menu_frames = {}
        self.terminal_frame = TerminalFrame(master=self)
        self.terminal_output = TerminalOutput(master=self.terminal_frame)
        self.terminal_output.tag_config("title", foreground="#FFD700")
        self.terminal_output.tag_config("info", foreground="white")
        self.terminal_output.tag_config("error", foreground="#FF4C4C")
        self._create_all_menus()
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
                command=lambda: self.show_menu("main"),
                row=last_row,
            )
        return frame

    def _create_all_menus(self):
        buttonsMainDict = MenuMain(self)
        buttonsMain = list(buttonsMainDict.items())
        main_frame = self._create_menu_generic(
            "main", "Menu Principal", buttonsMain, notMain=False
        )
        BaseButton(
            main_frame,
            text="Sair",
            command=self.quit,
            row=len(buttonsMain) + 2,
        )

        sub_menus = [
            ("info_diag", "Informações do Sistema", MenuInfoDiag),
            ("relatory", "Relatórios", MenuRelatory),
            ("show_logs", "Visualizar Logs", MenuShowLogs),
            ("show_lists", "Listas", MenuShowLists),
            ("manut_otim", "Manutenção e Otimização", MenuManutOtim),
            ("clean_archives", "Limpeza de Arquivos", MenuCleanArchives),
            ("otim_disk", "Otimização de Disco", MenuOtimDisk),
            ("fix_sistem", "Reparo do Sistema", MenuFixSistem),
            (
                "check_integrity",
                "Verificação de Integridade",
                MenuCheckIntegrity,
            ),
            (
                "repair_components",
                "Reparo de Componentes",
                MenuRepairComponents,
            ),
            ("restore_points", "Pontos de Restauração", MenuRestorePoints),
            ("network", "Rede e Internet", MenuNetwork),
            ("network_diag", "Diagnóstico de Rede", MenuNetworkDiag),
            ("network_fix", "Reparo de Rede", MenuNetworkFix),
            ("network_config", "Configurações de Rede", MenuNetworkConfig),
            ("firewall", "Firewall", MenuFirewall),
            ("security", "Segurança", MenuSecurity),
            ("admin_system", "Administração do Sistema", MenuAdminSystem),
            ("admin_tools", "Ferramentas Administrativas", MenuAdminTools),
            (
                "user_management",
                "Gerenciamento de Usuários",
                MenuUserManagement,
            ),
            (
                "interface_settings",
                "Configurações de Interface",
                MenuInterfaceSettings,
            ),
            ("general_settings", "Configurações Gerais", MenuGeneralSettings),
            ("soft_app", "Software e Aplicativos", MenuSoftApp),
            (
                "install_programs",
                "Instalar Programas (Winget)",
                MenuInstallPrograms,
            ),
        ]

        for name, title, menu_func in sub_menus:
            buttons_dict = menu_func(self)
            buttons_list = list(buttons_dict.items())
            self._create_menu_generic(name, title, buttons_list)

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

    def run_powershell_in_thread(self, command, task_name, admin=False):
        self._show_header(task_name, admin)

        def _threaded_task_runner():
            process = None
            try:
                full_command = self._prepare_powershell_command(command)
                process = self._execute_subprocess_realtime(full_command)
                self._read_stream_and_update_gui(process.stdout)
            except FileNotFoundError:
                self._show_errors("ERRO: O PowerShell não foi encontrado.")
            except Exception as exc:
                self._show_errors(f"Ocorreu um erro inesperado: {exc}")
            finally:
                if process:
                    self._handle_process_completion(process, task_name)

        self._run_thread(_threaded_task_runner)


if __name__ == "__main__":
    app = WorkbenchForWindows()
    app.mainloop()
