"""Caesar shift analysis and automated candidate scoring."""

from dataclasses import dataclass
from typing import List

from haxmed_cryptolab.engines.analysis.frequency import FrequencyAnalyzer
from haxmed_cryptolab.engines.classical.caesar import CaesarCipher


@dataclass
class CaesarCandidate:
    shift: int
    plaintext: str
    chi_squared: float
    rank: int = 0


class CaesarAnalyzer:
    """Evaluates and ranks all 26 Caesar rotations against natural English frequencies."""

    @classmethod
    def analyze_all_shifts(cls, ciphertext: str) -> List[CaesarCandidate]:
        """
        Decrypt ciphertext for shifts 0 through 25, compute Chi-Squared score for each,
        and return sorted candidates from most likely (lowest Chi-Squared) to least likely.
        """
        candidates: List[CaesarCandidate] = []

        for shift in range(26):
            candidate_text = CaesarCipher.decrypt(ciphertext, shift)
            chi_sq = FrequencyAnalyzer.calculate_chi_squared(candidate_text)
            candidates.append(
                CaesarCandidate(
                    shift=shift,
                    plaintext=candidate_text,
                    chi_squared=chi_sq,
                )
            )

        # Sort ascending by Chi-Squared score (best English fit first)
        candidates.sort(key=lambda c: c.chi_squared)

        for rank, candidate in enumerate(candidates, start=1):
            candidate.rank = rank

        return candidates
