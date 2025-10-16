import webview
import re
import os
import sys
from datetime import datetime
from src.scripts import ScriptsMixin
from src.interface import InterfaceMixin
from src.menu import (
    MenuMain, MenuInfoDiag, MenuRelatory, MenuShowLogs, MenuShowLists,
    MenuManutOtim, MenuCleanArchives, MenuOtimDisk, MenuFixSistem,
    MenuCheckIntegrity, MenuRepairComponents, MenuRestorePoints,
    MenuNetwork, MenuNetworkDiag, MenuNetworkFix, MenuNetworkConfig,
    MenuFirewall, MenuSecurity, MenuAdminSystem, MenuAdminTools,
    MenuUserManagement, MenuInterfaceSettings, MenuGeneralSettings,
    MenuSoftApp, MenuInstallPrograms,
)
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')


def _get_mapped_menu(menu_func, api_instance):
    mapped = {}
    try:
        menu = menu_func(api_instance)
        for key, item in menu.items():
            if hasattr(item, '__name__') and item.__name__ != '<lambda>':
                mapped[key] = item.__name__

            elif isinstance(item, tuple) and len(item) == 2 and item[
                0] == "show_menu":
                mapped[key] = f"show_menu_{item[1]}"

            else:
                func_name = None
                if hasattr(item, '__name__') and item.__name__ == '<lambda>':
                    func_str = str(item)
                    cleaned_func_str = re.sub(r'\s+', '', func_str)
                    match_name = re.search(r'self\.(\w+)\(', cleaned_func_str)
                    if match_name:
                        func_name = match_name.group(1)

                if func_name:
                    mapped[key] = func_name
                else:
                    logging.warning(f"Não foi possível mapear o item de menu '{key}'. Usando 'unknown_func'.")
                    mapped[key] = 'unknown_func'
    except Exception as e:
        logging.error(f"Erro ao mapear menu: {e}")
    return mapped


class WorkbenchApi(ScriptsMixin):

    def __init__(self, window):
        self.window = window
        self.interface_utils = InterfaceMixin()
        super().__init__()

    def get_menu_structure(self):
        menu_structure = {
            "main": _get_mapped_menu(MenuMain, self),
            "info_diag": _get_mapped_menu(MenuInfoDiag, self),
            "relatory": _get_mapped_menu(MenuRelatory, self),
            "show_logs": _get_mapped_menu(MenuShowLogs, self),
            "show_lists": _get_mapped_menu(MenuShowLists, self),
            "manut_otim": _get_mapped_menu(MenuManutOtim, self),
            "clean_archives": _get_mapped_menu(MenuCleanArchives, self),
            "otim_disk": _get_mapped_menu(MenuOtimDisk, self),
            "fix_sistem": _get_mapped_menu(MenuFixSistem, self),
            "check_integrity": _get_mapped_menu(MenuCheckIntegrity, self),
            "repair_components": _get_mapped_menu(MenuRepairComponents, self),
            "restore_points": _get_mapped_menu(MenuRestorePoints, self),
            "network": _get_mapped_menu(MenuNetwork, self),
            "network_diag": _get_mapped_menu(MenuNetworkDiag, self),
            "network_fix": _get_mapped_menu(MenuNetworkFix, self),
            "network_config": _get_mapped_menu(MenuNetworkConfig, self),
            "firewall": _get_mapped_menu(MenuFirewall, self),
            "security": _get_mapped_menu(MenuSecurity, self),
            "admin_system": _get_mapped_menu(MenuAdminSystem, self),
            "admin_tools": _get_mapped_menu(MenuAdminTools, self),
            "user_management": _get_mapped_menu(MenuUserManagement, self),
            "interface_settings": _get_mapped_menu(MenuInterfaceSettings,
                                                   self),
            "general_settings": _get_mapped_menu(MenuGeneralSettings, self),
            "soft_app": _get_mapped_menu(MenuSoftApp, self),
            "install_programs": _get_mapped_menu(MenuInstallPrograms, self),
        }
        return menu_structure

    def save_terminal_log(self, log_content):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"log_Ferramentas_{timestamp}.txt"
            base_dir = os.path.dirname(sys.argv[0])
            log_path = os.path.join(base_dir, filename)
            cleaned_content = re.sub(r'\[(TITLE|ERROR|INFO|DEBUG)]\s?', '', log_content, flags=re.IGNORECASE)
            cleaned_content = cleaned_content.lstrip('\n')
            with open(log_path, "w", encoding="utf-8") as f:
                f.write("Log de Sessão - Ferramentas (Web)\n")
                f.write("-" * 40 + "\n\n")
                f.write(cleaned_content)
            logging.info(f"Log de terminal salvo com sucesso em: {log_path}")
            self._safe_exit()
            return True
        except Exception as e:
            logging.error(f"ERRO ao salvar o log: {e}")
            self._safe_exit()
            return False

    def _safe_exit(self):
        logging.info("Finalizando processo Python.")
        if self.window:
            self.window.destroy()
        sys.exit(0)

    def quit(self):
        self._safe_exit()


def start_app():
    try:
        api = WorkbenchApi(None)
        window = webview.create_window(
            'Ferramentas - Windows (Web)',
            url="./src/index.html",
            js_api=api,
            width=1200,
            height=700,
            resizable=True,
            minimized=False,
            maximized=True,
        )
        api.window = window
        webview.start()
    except Exception as e:
        logging.critical(f"Falha ao iniciar o aplicativo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    start_app()