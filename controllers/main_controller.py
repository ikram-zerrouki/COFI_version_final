from PyQt5.QtCore import QObject, pyqtSignal
from models.analysis_model import AnalysisModel
from controllers.file_controller import FileController
from controllers.export_controller import ExportController


class MainController(QObject):
    operation_completed = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.model = AnalysisModel()
        self.file_controller = FileController(self)
        self.export_controller = ExportController(self)
        self.model.data_updated.connect(lambda: self.operation_completed.emit(True, "Données mises à jour"))

    def get_raw_data(self):
        return self.model.raw_data

    def get_processed_data(self):
        return self.model.processed_data

    def get_trends(self):
        return self.model.trends