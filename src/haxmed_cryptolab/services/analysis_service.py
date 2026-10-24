"""Service coordinating classical cipher cryptanalysis."""

from typing import Dict, List, Tuple

from haxmed_cryptolab.engines.analysis.caesar_analyzer import CaesarAnalyzer, CaesarCandidate
from haxmed_cryptolab.engines.analysis.frequency import FrequencyAnalyzer


class AnalysisService:
    """Orchestrates frequency analysis and classical cipher cracking heuristics."""

    @staticmethod
    def analyze_frequencies(text: str) -> Tuple[Dict[str, int], Dict[str, float], float, int]:
        """
        Compute letter counts, percentages, Index of Coincidence, and total letter count.
        Returns (counts, percentages, ioc, total_letters).
        """
        counts, percentages, total = FrequencyAnalyzer.calculate_frequencies(text)
        ioc = FrequencyAnalyzer.calculate_index_of_coincidence(text)
        return counts, percentages, ioc, total

    @staticmethod
    def analyze_caesar_shifts(ciphertext: str) -> List[CaesarCandidate]:
        """Evaluate all 26 Caesar rotations and rank by English frequency similarity."""
        return CaesarAnalyzer.analyze_all_shifts(ciphertext)
