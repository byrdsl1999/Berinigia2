from collections import Counter
import math

class Calculator:
    def __init__(self, species_counts=None):
        """
        Initialize the DiversityCalculator with a Counter of species counts.

        Args:
            species_counts (Counter): A Counter object with species counts.
        """
        self.species_counts = species_counts

    def richness(self):
        total_species = len(self.species_counts)
        return total_species

    def shannon_diversity_index(self):
        """
        Calculate the Shannon Diversity Index (H).

        Returns:
            float: Shannon Diversity Index (H).
        """
        total_count = sum(self.species_counts.values())
        shannon_index = 0.0
        for count in self.species_counts.values():
            p_i = count / total_count
            shannon_index -= p_i * math.log(p_i)
        return shannon_index

    def simpsons_diversity_index(self):
        """
        Calculate Simpson's Diversity Index (D).

        Returns:
            float: Simpson's Diversity Index (D).
        """
        total_count = sum(self.species_counts.values())
        simpsons_index = 0.0
        for count in self.species_counts.values():
            p_i = count / total_count
            simpsons_index += p_i**2
        return 1 / simpsons_index

    def pielous_evenness_index(self):
        """
        Calculate Pielou's Evenness Index (J).

        Returns:
            float: Pielou's Evenness Index (J).
        """
        total_count = sum(self.species_counts.values())

        # Handle the case of a unispecies system
        if len(self.species_counts) == 1:
            return 1.0  # Pielou's Evenness is 1 for a single species system

        shannon_index = self.shannon_diversity_index()
        max_shannon_index = math.log(len(self.species_counts))
        pielous_evenness = shannon_index / max_shannon_index
        return pielous_evenness
