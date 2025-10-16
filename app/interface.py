import subprocess
import threading
from datetime import datetime
import os


class InterfaceMixin:
    def _decode_output(self, data):
        if not data:
            return ""
        for encoding in ["utf-8", "cp850", "latin1"]:
            try:
                return data.decode(encoding).replace("\ufeff", "").strip()
            except UnicodeDecodeError:
                continue
        return (
            data.decode("latin1", errors="replace")
            .replace("\ufeff", "")
            .strip()
        )

    def _execute_subprocess_realtime(self, full_command):
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(
            full_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            startupinfo=startupinfo,
        )
        return process

    def show_menu(self, name_menu):
        frame = self.menu_frames[name_menu]
        frame.tkraise()

    def show_on_terminal(self, text, tag="info"):
        if not text.strip():
            return
        self.terminal_output.configure(state="normal")
        self.terminal_output.insert("end", text + "\n", (tag,))
        self.terminal_output.see("end")
        self.terminal_output.configure(state="disabled")

    def start_end(self):
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        text_init = f"====== Ferramentas - Windows ======\nData: {date_now}\n"
        text_init += "===========================\n"
        text_init += "Selecione uma opção no menu à esquerda"
        self.show_on_terminal(text_init, tag="title")

    def _show_header(self, task_name, admin):
        admin_msg = " (Requer Admin)" if admin else ""
        self.show_on_terminal(
            f"\n--- INICIANDO: {task_name}{admin_msg} ---", tag="title"
        )

    def _show_errors(self, mensagem):
        self.show_on_terminal(mensagem, tag="error")

    def _run_thread(self, target):
        thread = threading.Thread(target=target, daemon=True)
        thread.start()

    def _read_stream_and_update_gui(self, stream):
        for line_bytes in iter(stream.readline, b""):
            decoded_line = self._decode_output(line_bytes)
            self.after(
                0,
                lambda line=decoded_line: self.show_on_terminal(line),
            )

    def _handle_process_completion(self, process, task_name):
        process.wait()
        error_output = self._decode_output(process.stderr.read())
        if error_output:
            self._show_errors(f"ERRO:\n{error_output}")
        self.after(
            0,
            lambda: self.show_on_terminal(
                f"--- CONCLUÍDO: {task_name} ---", tag="title"
            ),
        )
