# interface.py (Corrigido com Mixin)

import subprocess
import threading
from datetime import datetime


class InterfaceMixin:
    """
    Mixin que contém todos os métodos relacionados à interação com a GUI.
    """

    def _decode_output(self, data):
        if not data:
            return ""
        for encoding in ["utf-8", "cp1252", "latin1"]:
            try:
                return data.decode(encoding).replace("\ufeff", "").strip()
            except UnicodeDecodeError:
                continue
        return (
            data.decode("latin1", errors="replace")
            .replace("\ufeff", "")
            .strip()
        )

    def _execute_subprocess(self, full_command):
        process = subprocess.run(
            full_command, capture_output=True, text=False, check=False
        )
        output = self._decode_output(process.stdout)
        error = self._decode_output(process.stderr)
        return output, error

    def _schedule_gui_updates(self, output, error, task_name):
        if output:
            self.show_on_terminal(output)
        if error:
            self.show_on_terminal(f"ERRO:\n{error}")
        self.show_on_terminal(f"--- CONCLUÍDO: {task_name} ---")

    def show_menu(self, name_menu):
        frame = self.menu_frames[name_menu]
        frame.tkraise()

    def show_on_terminal(self, text):
        if not text.strip():
            return
        self.terminal_output.configure(state="normal")
        self.terminal_output.insert("end", text + "\n")
        self.terminal_output.see("end")
        self.terminal_output.configure(state="disabled")

    def start_end(self):
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        texto_inicial = f"=== Ferramentas - Windows ===\nData: {data_atual}\n"
        texto_inicial += "============================\nSelecione uma opção no"
        texto_inicial += " menu à esquerda"
        self.show_on_terminal(texto_inicial)

    def _mostrar_header(self, task_name, admin):
        admin_msg = " (Requer Admin)" if admin else ""
        self.show_on_terminal(f"\n--- INICIANDO: {task_name}{admin_msg} ---")

    def _mostrar_erro(self, mensagem):
        self.show_on_terminal(mensagem)

    def _iniciar_thread(self, target):
        thread = threading.Thread(target=target, daemon=True)
        thread.start()
