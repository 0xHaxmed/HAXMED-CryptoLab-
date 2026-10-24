"""Candidate transformation rules for authorized hash recovery."""

from dataclasses import dataclass
from typing import Generator, Optional

from haxmed_cryptolab.core.exceptions import ValidationError


@dataclass
class RuleConfig:
    """Configuration options for candidate mutation rules."""

    apply_original: bool = True
    apply_lowercase: bool = False
    apply_uppercase: bool = False
    apply_capitalize: bool = False
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    append_numeric_range_end: int = 0  # 0 means disabled; e.g. 99 generates 0..99

    def validate(self):
        """Validate bounded parameters."""
        if self.append_numeric_range_end < 0 or self.append_numeric_range_end > 9999:
            raise ValidationError(
                "Numeric suffix range must be between 0 and 9999 to prevent unbounded workloads."
            )
        if self.prefix and len(self.prefix) > 64:
            raise ValidationError("Prefix length cannot exceed 64 characters.")
        if self.suffix and len(self.suffix) > 64:
            raise ValidationError("Suffix length cannot exceed 64 characters.")


class CandidateMutator:
    """Generates mutated candidate strings according to validated rules."""

    @classmethod
    def generate_mutations(cls, word: str, config: RuleConfig) -> Generator[str, None, None]:
        """Yield distinct candidate variations for a base word."""
        config.validate()
        base_forms = []

        if config.apply_original:
            base_forms.append(word)
        if config.apply_lowercase and word.lower() not in base_forms:
            base_forms.append(word.lower())
        if config.apply_uppercase and word.upper() not in base_forms:
            base_forms.append(word.upper())
        if config.apply_capitalize and word.capitalize() not in base_forms:
            base_forms.append(word.capitalize())

        # If no base form was selected, default to original
        if not base_forms:
            base_forms = [word]

        for base in base_forms:
            # 1. Base variation
            candidate = base
            if config.prefix:
                candidate = config.prefix + candidate
            if config.suffix:
                candidate = candidate + config.suffix

            yield candidate

            # 2. Bounded numeric suffixes if configured
            if config.append_numeric_range_end > 0:
                for num in range(config.append_numeric_range_end + 1):
                    yield f"{candidate}{num}"
