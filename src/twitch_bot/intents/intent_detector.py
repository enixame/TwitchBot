# intent_detector.py

from abc import ABC, abstractmethod

class IntentDetector(ABC):
    @abstractmethod
    def detect_intent(self, message_content):
        """Détecte l'intention dans le message.
        Cette méthode doit être implémentée par toutes les classes qui héritent de IntentDetector.
        """
        pass