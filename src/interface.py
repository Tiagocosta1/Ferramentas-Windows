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
