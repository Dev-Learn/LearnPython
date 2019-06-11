from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from googletrans import Translator

class WorkerTranslate(QObject):
    detectComplete = pyqtSignal(str, int, list, list)
    translateStatus = pyqtSignal(str, str)
    translateComplete = pyqtSignal(str, int)
    translateError = pyqtSignal(str)

    def __init__(self, detectLanguage: dict = None, translateLanguage: dict = None):
        super().__init__()
        self.translator = Translator()
        if detectLanguage:
            self.languageDetect = detectLanguage
        else:
            self.languageTranstate = translateLanguage

    @pyqtSlot()
    def detectLanguage(self):
        languageCode = self.translator.detect(self.languageDetect['text'])
        print(languageCode)
        self.detectComplete.emit(languageCode.lang, self.languageDetect['size'], self.languageDetect['listName'], self.languageDetect['listValue'])

    @pyqtSlot()
    def translateLanguage(self):
        try:
            for index, item in enumerate(self.languageTranstate['listResource']):
                self.translateStatus.emit(item, "")
                value = self.translator.translate(item, dest=self.languageTranstate['code'])
                value = value.text
                self.translateStatus.emit(item, value)
                print(value)
                self.translateComplete.emit(value, index)
        except ValueError as e:
            print(e)
            self.translateError.emit()
