"""Frequency distribution analysis and statistical scoring for classical ciphers."""

import string
from collections import Counter
from typing import Dict, Tuple

# Standard English letter frequencies (percentages summing to ~100.0)
ENGLISH_LETTER_FREQUENCIES: Dict[str, float] = {
    "A": 8.167,
    "B": 1.492,
    "C": 2.782,
    "D": 4.253,
    "E": 12.702,
    "F": 2.228,
    "G": 2.015,
    "H": 6.094,
    "I": 6.966,
    "J": 0.153,
    "K": 0.772,
    "L": 4.025,
    "M": 2.406,
    "N": 6.749,
    "O": 7.507,
    "P": 1.929,
    "Q": 0.095,
    "R": 5.987,
    "S": 6.327,
    "T": 9.056,
    "U": 2.758,
    "V": 0.978,
    "W": 2.360,
    "X": 0.150,
    "Y": 1.974,
    "Z": 0.074,
}

ENGLISH_INDEX_OF_COINCIDENCE = 0.0667


class FrequencyAnalyzer:
    """Calculates letter frequencies, percentages, and Index of Coincidence."""

    @staticmethod
    def calculate_frequencies(text: str) -> Tuple[Dict[str, int], Dict[str, float], int]:
        """
        Calculate raw counts and percentage frequencies for letters A-Z.
        Returns (counts_dict, percentage_dict, total_letters).
        """
        counts = {letter: 0 for letter in string.ascii_uppercase}
        total_letters = 0

        for char in text.upper():
            if char in counts:
                counts[char] += 1
                total_letters += 1

        percentages = {}
        for letter in string.ascii_uppercase:
            percentages[letter] = (
                (counts[letter] / total_letters * 100.0) if total_letters > 0 else 0.0
            )

        return counts, percentages, total_letters

    @staticmethod
    def calculate_index_of_coincidence(text: str) -> float:
        """
        Calculate the Index of Coincidence (IoC).
        IoC measures the probability that two randomly selected letters from the text are identical.
        For normal English text, IoC ≈ 0.0667.
        For random uniform distribution (polyalphabetic), IoC ≈ 0.0385.
        """
        counts = Counter([c.upper() for c in text if c.isalpha()])
        n = sum(counts.values())
        if n <= 1:
            return 0.0

        numerator = sum(count * (count - 1) for count in counts.values())
        denominator = n * (n - 1)
        return numerator / denominator

    @classmethod
    def calculate_chi_squared(cls, text: str) -> float:
        """
        Compute Chi-Squared statistic of the text compared to standard English letter distribution.
        Lower score indicates closer resemblance to natural English.
        """
        counts, _, total_letters = cls.calculate_frequencies(text)
        if total_letters == 0:
            return float("inf")

        chi_sq = 0.0
        for letter, expected_pct in ENGLISH_LETTER_FREQUENCIES.items():
            expected_count = (expected_pct / 100.0) * total_letters
            observed_count = counts[letter]
            chi_sq += ((observed_count - expected_count) ** 2) / expected_count

        return chi_sq
