"""Background worker for authorized hash recovery experiments."""

import time
from typing import Optional

from PySide6.QtCore import QThread, Signal

from haxmed_cryptolab.engines.recovery.adapters import BaseHashAdapter
from haxmed_cryptolab.engines.recovery.rules import CandidateMutator, RuleConfig
from haxmed_cryptolab.engines.recovery.wordlist import WordlistLoader
from haxmed_cryptolab.models import RecoveryCandidateMatch


class HashRecoveryWorker(QThread):
    """Executes wordlist iteration and rule transformations in a background thread."""

    progress_signal = Signal(int, int, float)  # attempts, total_base_candidates, candidates_per_sec
    match_found_signal = Signal(object)  # RecoveryCandidateMatch
    finished_signal = Signal(object, int, float)  # match_or_none, total_attempts, elapsed_seconds
    error_signal = Signal(str)

    def __init__(
        self,
        wordlist_path: str,
        target_hash: str,
        adapter: BaseHashAdapter,
        rule_config: RuleConfig,
        total_base_candidates: int,
        encoding: str = "utf-8",
        parent=None,
    ):
        super().__init__(parent)
        self.wordlist_path = wordlist_path
        self.target_hash = target_hash
        self.adapter = adapter
        self.rule_config = rule_config
        self.total_base_candidates = total_base_candidates
        self.encoding = encoding
        self._is_cancelled = False

    def cancel(self):
        self._is_cancelled = True

    def run(self):
        t0 = time.perf_counter()
        attempts = 0
        last_progress_time = t0
        found_match: Optional[RecoveryCandidateMatch] = None

        try:
            # Validate target hash format with the adapter first
            self.adapter.validate_target(self.target_hash)

            candidate_stream = WordlistLoader.stream_candidates(self.wordlist_path, self.encoding)

            for base_word in candidate_stream:
                if self._is_cancelled:
                    break

                for candidate in CandidateMutator.generate_mutations(base_word, self.rule_config):
                    if self._is_cancelled:
                        break

                    attempts += 1
                    if self.adapter.verify(candidate, self.target_hash):
                        elapsed = time.perf_counter() - t0
                        found_match = RecoveryCandidateMatch(
                            target_hash=self.target_hash,
                            plaintext=candidate,
                            rule_applied="Mutated Candidate",
                            attempts_evaluated=attempts,
                            time_elapsed_seconds=elapsed,
                        )
                        self.match_found_signal.emit(found_match)
                        break

                    # Update progress periodically (every 50ms or 100 attempts)
                    now = time.perf_counter()
                    if now - last_progress_time >= 0.1 or attempts % 100 == 0:
                        elapsed = now - t0
                        rate = (attempts / elapsed) if elapsed > 0 else 0.0
                        self.progress_signal.emit(attempts, self.total_base_candidates, rate)
                        last_progress_time = now

                if found_match:
                    break

            total_elapsed = time.perf_counter() - t0
            self.finished_signal.emit(found_match, attempts, total_elapsed)

        except Exception as e:
            self.error_signal.emit(str(e))
