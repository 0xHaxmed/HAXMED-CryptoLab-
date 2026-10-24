"""Service managing candidate recovery workflows, rule generation, and adapters."""

import json
from datetime import datetime
from typing import List, Optional, Tuple

from haxmed_cryptolab.core.config import ConfigManager
from haxmed_cryptolab.core.exceptions import ValidationError
from haxmed_cryptolab.engines.recovery.adapters import (
    Argon2idAdapter,
    BaseHashAdapter,
    BcryptAdapter,
    RawDigestAdapter,
)
from haxmed_cryptolab.engines.recovery.rules import RuleConfig
from haxmed_cryptolab.engines.recovery.wordlist import WordlistLoader
from haxmed_cryptolab.models import RecoveryCandidateMatch
from haxmed_cryptolab.storage.history_repository import HistoryRepository


class RecoveryService:
    """Orchestrates candidate wordlist processing, transformations, and adapters."""

    def __init__(
        self,
        history_repo: Optional[HistoryRepository] = None,
        config_mgr: Optional[ConfigManager] = None,
    ):
        self.history_repo = history_repo or HistoryRepository()
        self.config_mgr = config_mgr or ConfigManager()

    @staticmethod
    def get_adapter(adapter_name: str, raw_algo: str = "SHA-256") -> BaseHashAdapter:
        """Instantiate the matching recovery adapter."""
        norm = adapter_name.strip().lower()
        if "bcrypt" in norm:
            return BcryptAdapter()
        elif "argon2" in norm:
            return Argon2idAdapter()
        elif "raw" in norm or "digest" in norm:
            return RawDigestAdapter(algorithm=raw_algo)
        else:
            raise ValidationError(f"Unknown recovery adapter: '{adapter_name}'.")

    @staticmethod
    def inspect_wordlist(file_path: str) -> Tuple[int, List[str], str]:
        """Count entries, extract samples, and detect encoding."""
        return WordlistLoader.count_and_sample(file_path)

    @classmethod
    def generate_sanitized_report(
        cls,
        target_hash: str,
        adapter_name: str,
        wordlist_name: str,
        total_evaluated: int,
        elapsed_seconds: float,
        match: Optional[RecoveryCandidateMatch],
        rule_config: RuleConfig,
        format_type: str = "txt",
    ) -> str:
        """
        Generate a sanitized audit report of the recovery experiment.
        Avoids leaking full passwords if requested.
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        status = "MATCH FOUND" if match else "NO MATCH IDENTIFIED"
        cands_per_sec = (total_evaluated / elapsed_seconds) if elapsed_seconds > 0 else 0.0

        if format_type.lower() == "json":
            report_data = {
                "report_title": "HAXMED CryptoLab — Hash Recovery Lab Audit Report",
                "timestamp": timestamp,
                "status": status,
                "target_hash": target_hash,
                "adapter": adapter_name,
                "wordlist": wordlist_name,
                "total_evaluated": total_evaluated,
                "elapsed_seconds": round(elapsed_seconds, 3),
                "candidates_per_second": round(cands_per_sec, 1),
                "rule_configuration": {
                    "original": rule_config.apply_original,
                    "lowercase": rule_config.apply_lowercase,
                    "uppercase": rule_config.apply_uppercase,
                    "capitalize": rule_config.apply_capitalize,
                    "prefix": rule_config.prefix or "",
                    "suffix": rule_config.suffix or "",
                    "numeric_range_end": rule_config.append_numeric_range_end,
                },
                "match_details": {
                    "rule_applied": match.rule_applied if match else None,
                    "attempts_at_match": match.attempts_evaluated if match else None,
                }
                if match
                else None,
            }
            return json.dumps(report_data, indent=2)

        # Plain Text format
        lines = [
            "=======================================================================",
            "             HAXMED CryptoLab — Hash Recovery Lab Audit Report",
            "=======================================================================",
            f"Timestamp:              {timestamp}",
            f"Execution Outcome:      {status}",
            f"Target Hash:            {target_hash}",
            f"Algorithm / Adapter:    {adapter_name}",
            f"Wordlist Source:        {wordlist_name}",
            f"Total Candidates Tried: {total_evaluated:,}",
            f"Time Elapsed:           {elapsed_seconds:.2f} seconds",
            f"Verification Speed:     {cands_per_sec:,.1f} candidates/sec",
            "-----------------------------------------------------------------------",
            "Transformation Rules:",
            f"  - Lowercase / Upper / Capitalize: {rule_config.apply_lowercase} / {rule_config.apply_uppercase} / {rule_config.apply_capitalize}",
            f"  - Fixed Prefix: {rule_config.prefix or '(none)'}",
            f"  - Fixed Suffix: {rule_config.suffix or '(none)'}",
            f"  - Numeric Suffix Range: 0..{rule_config.append_numeric_range_end}",
            "-----------------------------------------------------------------------",
        ]
        if match:
            lines.extend(
                [
                    "Match Result:           CANDIDATE VERIFIED",
                    f"Rule Applied:           {match.rule_applied}",
                    f"Evaluated At Attempt:   {match.attempts_evaluated:,}",
                    "-----------------------------------------------------------------------",
                    "NOTE: Candidate verification confirms mathematical hash equivalence.",
                ]
            )
        else:
            lines.extend(
                [
                    "Match Result:           NO MATCH IN SEARCH SPACE",
                    "NOTE: Target was not matched within the loaded wordlist and configured rules.",
                ]
            )
        lines.append("=======================================================================")
        return "\n".join(lines)
