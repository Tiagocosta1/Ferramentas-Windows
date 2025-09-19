def MenuMain(self):
    return {
        "Informações E Diagnóstico": lambda: self.show_menu("info_diag"),
        "Manutenção e Otimização": lambda: self.show_menu("manut_otim"),
        "Reparo do Sistema": lambda: self.show_menu("fix_sistem"),
        "Rede e Internet": lambda: self.show_menu("network"),
        "Segurança": lambda: self.show_menu("security"),
        "Administração do Sistema": lambda: self.show_menu("admin_system"),
        "Software e Aplicativos (Winget)": lambda: self.show_menu("soft_app"),
    }


def MenuInfoDiag(self):
    return {
        "Informações do Sistema": self.get_system_info,
        "Relatórios": lambda: self.show_menu("relatory"),
        "Visualizar Logs": lambda: self.show_menu("show_logs"),
        "Listas": lambda: self.show_menu("show_lists"),
    }


def MenuRelatory(self):
    return {
        "Relatório de Energia": self.logs_energy,
        "Status da Licença (Windows)": self.status_windows,
        "Teste de Velocidade do Disco": self.speed_disk,
    }


def MenuShowLogs(self):
    return {
        "Logs de Aplicativos": self.logs_app,
        "Logs de Atualizações (Windows)": self.logs_update,
        "Logs (Geral)": self.logs_windows,
    }


def MenuShowLists(self):
    return {
        "Lista de Usuários": self.get_user_info,
        "Lista Programas (Logon)": self.list_startup_run,
    }


def MenuManutOtim(self):
    return {
        "Rotina de Limpeza Completa": self.clean_full,
        "Limpeza de Arquivos": lambda: self.show_menu("clean_archives"),
        "Otimização de Disco": lambda: self.show_menu("otim_disk"),
    }


def MenuCleanArchives(self):
    return {
        "Limpar Arquivos Temporários": self.clean_temp_files,
        "Limpar Cache (Navegadores)": self.clean_browsers,
        "Limpeza de Disco (cleanmgr)": self.clean_disk,
        "Limpar Logs (Ação)": self.clean_logs,
    }


def MenuOtimDisk(self):
    return {
        "Otimizar Disco (Desfrag/TRIM)": self.defrag_disk,
        "Compactar Windows": self.compact_os,
    }


def MenuFixSistem(self):
    return {
        "Rotina de Reparo de Sistema(DISM+SFC)": self.fix_full,
        "Verificadores de Integridade": lambda: self.show_menu(
            "check_integrity"
        ),
        "Reparo de Componentes": lambda: self.show_menu("repair_components"),
        "Ponto de Restauração": lambda: self.show_menu("restore_points"),
        "Diagnostoco de Memória": self.diag_memory,
        "Backup de Drivers": self.backup_driver,
    }


def MenuCheckIntegrity(self):
    return {
        "Verificar Sistema (sfc)": self.run_sfc,
        "Verificar Integridade (dism)": self.run_dism,
        "Verificar Disco (chkdsk)": self.run_chkdsk,
    }


def MenuRepairComponents(self):
    return {
        "Limpar Fila de Impressão": self.clear_print_queue,
        "Reparar Windows Update": self.fix_windows_update,
        "Reparar Firewall": self.fix_firewall,
        "Reparar Rede": self.fix_network,
        "Reparar Ícones": self.fix_icons,
        "Reparar Menu Iniciar": self.fix_start_menu,
        "Reparar Barra de Tarefas": self.fix_taskbar,
        "Reparar Microsoft Store": self.fix_microsoft_store,
        "Re-registrar Apps da Store": self.re_register_store_apps,
    }


def MenuRestorePoints(self):
    return {
        "Ativar Restauração do Sistema": self.enable_system_restore,
        "Desativar Restauração do Sistema": self.disable_system_restore,
        "Criar Ponto de Restauração": self.point_restore,
        "Restaurar Sistema": self.restore_system,
    }


def MenuNetwork(self):
    return {
        "Diagnóstico de Rede": lambda: self.show_menu("network_diag"),
        "Reparo de Rede": lambda: self.show_menu("network_fix"),
        "Configurações de Rede": lambda: self.show_menu("network_config"),
    }


def MenuNetworkDiag(self):
    return {
        "IP Atual": self.get_network_info,
        "Listar Placas de Rede": self.list_networks,
        "Teste Ping(8.8.8.8)": self.test_ping_dns,
        "Teste Ping(google.com)": self.test_ping_page,
        "Ratrear Rota(google.com)": self.get_routes,
    }


def MenuNetworkFix(self):
    return {
        "Redefinir IP": self.clean_ip,
        "Redefinir Winsock": self.clean_winsock,
        "Limpar Cache DNS": self.clean_dns,
    }


def MenuNetworkConfig(self):
    return {
        "Desativar IPv6": self.disable_ipv6,
        "Firewall": lambda: self.show_menu("firewall"),
    }


def MenuFirewall(self):
    return {
        "Status do Firewall": self.status_firewall,
        "Ativar Firewall": self.ativ_firewall,
        "Desativar Firewall": self.desativ_firewall,
    }


def MenuSecurity(self):
    return {
        "Status da Proteção": self.status_protection,
        "Atualizar Definições": self.update_definitions,
        "Verificação rápida de Ameaças": self.scan_threats,
        "Status do BitLocker": self.status_bitlocker,
    }


def MenuAdminSystem(self):
    return {
        "Ferramentas Administrativas": lambda: self.show_menu("admin_tools"),
        "Gerenciamento de Usuários": lambda: self.show_menu("user_management"),
        "Configurações de Interface": lambda: self.show_menu(
            "interface_settings"
        ),
        "Configurações Gerais": lambda: self.show_menu("general_settings"),
        "Ativ(win-off)": self.ativ_win_off,
    }


def MenuAdminTools(self):
    return {
        "Gerenciador de Dispositivos": self.device_manager,
        "Gerenciamento de Disco": self.disk_management,
        "Gerenciamento de Impressoras": self.printer_management,
        "Visualizador de Eventos": self.event_viewer,
        "Agendador de Tarefas": self.task_scheduler,
        "Serviços do Sistema": self.system_services,
        "Editor de Políticas de Grupo": self.group_policy_editor,
        "Editor do Registro": self.registry_editor,
    }


def MenuUserManagement(self):
    return {
        "Adicionar Usuário (Impressora)": self.create_user,
        "Gerenciar Usuários (local)": self.manager_users,
    }


def MenuInterfaceSettings(self):
    return {
        "Configurar Cores": self.ativ_color_theme,
        "Ativa Atalhos Sistema": self.ativ_shortcut,
        "Criar Atalhos do Office": self.shortcut_office,
        "Configurar Explorador de Arquivos": self.config_file_explorer,
        "Mostrar Arquivos Ocultos": self.show_hidden_files,
        "Ocultar Arquivos Ocultos": self.hide_hidden_files,
        "Configurar Opções Visuais": self.config_visual_options,
    }


def MenuGeneralSettings(self):
    return {
        "Data e Hora": self.config_date_time,
        "Plano de Energia": self.config_energy,
        "Desativar Notificações": self.disable_notifications,
    }


def MenuSoftApp(self):
    return {
        "Listar Programas(winget)": self.list_programs,
        "Instalar Programas": lambda: self.show_menu("install_programs"),
        "Remover Programas": self.remove_programs,
        "Remover Bloatware (Apps Windows)": self.remove_bloatware,
        "Atualizar Programs(winget)": self.update_winget,
        "Atualizar WinRar": self.ativ_winrar,
        "Atualizar Anydesk": self.renew_anydesk,
    }


def MenuInstallPrograms(self):
    return {
        "Adobe Reader": self.install_adobe_reader,
        "Foxit Reader": self.install_foxit,
        "Chrome": self.install_chrome,
        "Firefox": self.install_firefox,
        "Java": self.install_java,
        "K-Lite Codec": self.install_codec,
        "Microsoft Office": self.install_office,
        "AnyDesk": self.install_anydesk,
        "HopToDesk": self.install_hoptodesk,
        "Team Viewer": self.install_teamviewer,
        "7zip": self.install_7zip,
        "WinRar": self.install_winrar,
        "FastCopy": self.install_fastcopy,
    }
