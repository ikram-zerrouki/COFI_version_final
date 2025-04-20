from PyQt5.QtWidgets import (QWidget, QTabWidget, QSizePolicy, QVBoxLayout)
from ui.data_input import DataInputForm
from ui.results_view import ResultsView


class FinancialAnalysisView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.tabs)

        # Data input tab
        self.data_input = DataInputForm()
        self.data_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabs.addTab(self.data_input, "Saisie des Données")

        # Results tab
        self.results_view = ResultsView()
        self.results_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabs.addTab(self.results_view, "Résultats et Graphiques")

    def show_results_tab(self):
        """Switch to the results tab programmatically"""
        self.tabs.setCurrentIndex(1)

    def get_input_data(self):
        """Delegate to data_input component"""
        return self.data_input.get_input_data()