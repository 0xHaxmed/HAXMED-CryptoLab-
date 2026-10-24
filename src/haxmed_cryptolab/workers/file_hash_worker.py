"""Background worker for streaming file hash calculation."""

from PySide6.QtCore import QThread, Signal

from haxmed_cryptolab.services.hash_service import HashService


class FileHashWorker(QThread):
    """Executes chunked file hashing in a dedicated thread."""

    progress_signal = Signal(int, int)  # bytes_read, total_bytes
    finished_signal = Signal(object)  # HashResult
    error_signal = Signal(str)  # error message

    def __init__(
        self,
        hash_service: HashService,
        file_path: str,
        algorithm: str,
        chunk_size_kb: int = 64,
        parent=None,
    ):
        super().__init__(parent)
        self.hash_service = hash_service
        self.file_path = file_path
        self.algorithm = algorithm
        self.chunk_size_kb = chunk_size_kb
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        def progress_cb(read_b: int, total_b: int):
            self.progress_signal.emit(read_b, total_b)

        def cancel_check() -> bool:
            return self._is_cancelled

        try:
            result = self.hash_service.hash_file(
                file_path=self.file_path,
                algorithm=self.algorithm,
                chunk_size_kb=self.chunk_size_kb,
                progress_callback=progress_cb,
                cancel_check=cancel_check,
            )
            if not self._is_cancelled:
                self.finished_signal.emit(result)
        except InterruptedError:
            self.error_signal.emit("File hashing cancelled by user.")
        except Exception as e:
            self.error_signal.emit(str(e))
