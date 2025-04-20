"""from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from ui.home_tab import HomeTab
from ui.data_tab import DataTab
from ui.results_tab import ResultsTab
from ui.graphs_tab import GraphsTab
from ui.financial_analysis_view import FinancialAnalysisView



class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Analyse Comptable")
        self.setGeometry(100, 100, 1000, 700)
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()
        self.home_tab = HomeTab(self.controller)
        self.data_tab = DataTab(self.controller)
        self.results_tab = ResultsTab(self.controller)
        self.graphs_tab = GraphsTab(self.controller)

        self.tab_widget.addTab(self.home_tab, "Accueil")
        self.tab_widget.addTab(self.data_tab, "Données")
        self.tab_widget.addTab(self.results_tab, "Résultats")
        self.tab_widget.addTab(self.graphs_tab, "Graphiques")

        layout.addWidget(self.tab_widget)

    def _connect_signals(self):
        self.controller.operation_completed.connect(self._update_ui)

    def _update_ui(self, success, message):
        if success:
            self.data_tab.update_data()
            self.results_tab.update_results()
            self.graphs_tab.update_graphs()"""

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from ui.home_tab import HomeTab
from ui.data_tab import DataTab
from ui.results_tab import ResultsTab
from ui.graphs_tab import GraphsTab
from ui.financial_analysis_view import FinancialAnalysisView
from controllers.tab_controller import TabController  # Nouvel import


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Analyse Comptable")
        self.setGeometry(100, 100, 1200, 800)  # Augmentez la taille pour accommoder le nouvel onglet
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()

        # Onglets existants
        self.home_tab = HomeTab(self.controller)
        self.data_tab = DataTab(self.controller)
        self.results_tab = ResultsTab(self.controller)
        self.graphs_tab = GraphsTab(self.controller)

        # Onglet d'analyse financière
        self.financial_tab_controller = TabController()  # Créez le contrôleur
        self.financial_tab = self.financial_tab_controller.get_view()  # Obtenez la vue

        # Ajout des onglets
        self.tab_widget.addTab(self.home_tab, "Accueil")
        self.tab_widget.addTab(self.data_tab, "Données")
        self.tab_widget.addTab(self.results_tab, "Résultats")
        self.tab_widget.addTab(self.graphs_tab, "Graphiques")
        self.tab_widget.addTab(self.financial_tab, "Analyse Financière")  # Nouvel onglet

        layout.addWidget(self.tab_widget)

    def _connect_signals(self):
        self.controller.operation_completed.connect(self._update_ui)
        # Vous pouvez connecter d'autres signaux si nécessaire

    def _update_ui(self, success, message):
        if success:
            self.data_tab.update_data()
            self.results_tab.update_results()
            self.graphs_tab.update_graphs()
            # Mise à jour de l'onglet financier si nécessaire