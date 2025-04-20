from PyQt5.QtWidgets import (QWidget, QLabel, QTreeWidget, QTreeWidgetItem,
                             QComboBox, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QSizePolicy, QHeaderView)
from PyQt5.QtCore import pyqtSignal, Qt
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from utils.constants import *


class ResultsView(QWidget):
    graph_type_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.graph_data = None
        self.current_graph_type = 'liquidity'
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Results table
        results_group = QGroupBox("Ratios Financiers")
        results_layout = QVBoxLayout()

        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Description", f"Valeur ({CURRENCY})", "Pourcentage", "Interprétation"])
        self.results_tree.setColumnWidth(0, 350)
        self.results_tree.setColumnWidth(1, 150)
        self.results_tree.setColumnWidth(2, 100)
        self.results_tree.setColumnWidth(3, 400)
        self.results_tree.header().setSectionResizeMode(3, QHeaderView.Stretch)
        results_layout.addWidget(self.results_tree)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        # Graph
        graph_group = QGroupBox("Visualisation")
        graph_layout = QVBoxLayout()

        # Graph controls
        controls_layout = QHBoxLayout()
        self.graph_selector = QComboBox()
        self.graph_selector.addItems(["Liquidité", "Solvabilité", "Rentabilité", "Activité"])
        self.graph_selector.currentTextChanged.connect(self.on_graph_type_changed)
        controls_layout.addWidget(QLabel("Type de graphique:"))
        controls_layout.addWidget(self.graph_selector)
        controls_layout.addStretch()

        graph_layout.addLayout(controls_layout)

        # Create figure and canvas
        self.figure = Figure(figsize=(10, 4), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)

        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        self.setLayout(layout)

    def on_graph_type_changed(self, text):
        mapping = {
            "Liquidité": "liquidity",
            "Solvabilité": "solvency",
            "Rentabilité": "profitability",
            "Activité": "activity"
        }
        self.current_graph_type = mapping.get(text, "liquidity")
        self.update_graph()

    def display_results(self, ratios):
        self.results_tree.clear()

        for category, category_ratios in ratios.items():
            category_item = QTreeWidgetItem([CATEGORY_NAMES.get(category, category), "", "", ""])
            category_item.setFlags(category_item.flags() | Qt.ItemIsTristate)

            for ratio_name, ratio_data in category_ratios.items():
                value = ratio_data['value']
                description = ratio_data['description']
                components = ratio_data['components']

                # Format components for display
                if isinstance(components, tuple):
                    components_str = f"{components[0]:,.2f} / {components[1]:,.2f}"
                else:
                    components_str = f"{components:,.2f}"

                # Get interpretation based on ratio type
                if category == 'liquidity':
                    interpretation = get_interpretation(value, LIQUIDITY_THRESHOLDS)
                elif category == 'solvency':
                    if ratio_name == 'debt_to_equity':
                        interpretation = get_interpretation(value, DEBT_EQUITY_THRESHOLDS)
                    elif ratio_name == 'financial_leverage':
                        interpretation = get_interpretation(value, LEVERAGE_THRESHOLDS)
                    else:
                        interpretation = get_interpretation(value, INTEREST_COVERAGE_THRESHOLDS)
                elif category == 'profitability':
                    interpretation = get_interpretation(value, PROFITABILITY_THRESHOLDS)
                elif category == 'activity':
                    if ratio_name == 'inventory_turnover':
                        interpretation = get_interpretation(value, INVENTORY_TURNOVER_THRESHOLDS)
                    elif ratio_name == 'days_sales_outstanding':
                        interpretation = get_interpretation(value, DSO_THRESHOLDS)
                    else:
                        interpretation = get_interpretation(value, DPO_THRESHOLDS)
                else:
                    interpretation = "Non interprétable"

                # Format value display based on ratio type
                if ratio_name in ['days_sales_outstanding', 'days_payable_outstanding']:
                    value_str = f"{value:.1f} jours"
                elif ratio_name == 'inventory_turnover':
                    value_str = f"{value:.2f}x"
                else:
                    value_str = f"{value:.2%}"

                ratio_item = QTreeWidgetItem([
                    description,
                    components_str,
                    value_str,
                    interpretation
                ])
                category_item.addChild(ratio_item)

            self.results_tree.addTopLevelItem(category_item)

        self.results_tree.expandAll()

    def update_graph_data(self, graph_data):
        self.graph_data = graph_data
        self.update_graph()

    def update_graph(self):
        if not self.graph_data:
            return

        try:
            data = self.graph_data.get(self.current_graph_type, {})
            if not data:
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)

            # Create bar plot for ratios
            x = range(len(data['labels']))
            width = 0.35

            # Barres pour les ratios (pourcentages)
            bars1 = ax.bar(x, data['values'], width, color='skyblue', label='Ratio')
            ax.set_ylabel('Valeur du ratio')
            ax.set_title(data['title'])

            # Barres pour les montants (sur un second axe y)
            ax2 = ax.twinx()
            bars2 = ax2.bar([i + width for i in x], data['amounts'], width, color='orange',
                            label=f'Montant ({CURRENCY})')
            ax2.set_ylabel(f'Montant ({CURRENCY})')

            # Configuration des axes
            ax.set_xticks([i + width / 2 for i in x])
            ax.set_xticklabels(data['labels'], rotation=45, ha='right')

            # Ajout des valeurs sur les barres
            for bar in bars1:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height,
                        f'{height:.2%}',
                        ha='center', va='bottom')

            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2, height,
                         f'{height:,.2f}',
                         ha='center', va='bottom')

            # Légende combinée
            lines, labels = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines + lines2, labels + labels2, loc='upper right')

            self.figure.tight_layout()
            self.canvas.draw()
        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique: {str(e)}")