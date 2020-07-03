class LoanSource:
    def __init__(self, language, definition, native, transcription):
        self.language = language
        self.definition = definition
        self.native = native
        self.transcription = transcription

    def to_json(self):
        return {
            "definition": self.definition,
            "forms": {
                "$gn$": {
                    "native": self.native,
                    "transcription": self.transcription
                }
            }
        }