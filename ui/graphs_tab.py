from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class GraphsTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        # Zone défilante pour les graphiques
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Widget conteneur
        container = QWidget()
        self.layout = QVBoxLayout(container)

        # Bouton d'export
        export_btn = QPushButton("Exporter en PDF")
        export_btn.clicked.connect(self._export_pdf)

        # Zone pour les graphiques
        self.graphs_container = QVBoxLayout()
        self.graphs_container.setAlignment(Qt.AlignTop)

        self.layout.addWidget(export_btn)
        self.layout.addLayout(self.graphs_container)
        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def update_graphs(self):
        """Met à jour les 6 graphiques comme dans le code original"""
        # Nettoyer les anciens graphiques
        for i in reversed(range(self.graphs_container.count())):
            self.graphs_container.itemAt(i).widget().setParent(None)

        df = self.controller.get_processed_data()
        if df.empty:
            return

        # Graphique 1: Évolution du CA
        fig1 = Figure(figsize=(8, 4))
        ax1 = fig1.add_subplot(111)
        df['Chiffre_affaires'].plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_title('Évolution du Chiffre d\'Affaires')
        ax1.set_ylabel('Montant (DZD)')
        ax1.grid(True, alpha=0.3)
        canvas1 = FigureCanvas(fig1)
        self.graphs_container.addWidget(canvas1)

        # Graphique 2: Répartition des charges
        fig2 = Figure(figsize=(8, 4))
        ax2 = fig2.add_subplot(111)
        width = 0.35
        x = np.arange(len(df.index))
        ax2.bar(x, df['Charges_variables'] / 1_000_000, width, label='Charges variables')
        ax2.bar(x, df['Charges_fixes'] / 1_000_000, width,
                bottom=df['Charges_variables'] / 1_000_000, label='Charges fixes')
        ax2.set_title('Répartition des charges')
        ax2.set_ylabel('Millions DZD')
        ax2.set_xticks(x)
        ax2.set_xticklabels(df.index)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        canvas2 = FigureCanvas(fig2)
        self.graphs_container.addWidget(canvas2)

        # Graphique 3: Indicateurs de rentabilité
        fig3 = Figure(figsize=(8, 4))
        ax3 = fig3.add_subplot(111)
        ax3.plot(df.index, df['Taux_rentabilite'], marker='o', color='green', linewidth=2, label='Rentabilité')
        ax3.plot(df.index, df['ROE'], marker='s', color='red', linewidth=2, label='ROE')
        ax3.plot(df.index, df['ROA'], marker='^', color='blue', linewidth=2, label='ROA')
        ax3.set_title('Indicateurs de rentabilité')
        ax3.set_ylabel('Pourcentage (%)')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        canvas3 = FigureCanvas(fig3)
        self.graphs_container.addWidget(canvas3)

        # Graphique 4: Structure du bilan
        fig4 = Figure(figsize=(8, 4))
        ax4 = fig4.add_subplot(111)
        x_pos = np.arange(len(df.index))
        bar_width = 0.4
        actifs = [df.loc[year, 'Total_actif'] / 1_000_000 for year in df.index]
        passifs = [df.loc[year, 'Total_passif'] / 1_000_000 for year in df.index]
        ax4.bar(x_pos, actifs, width=bar_width, color='lightblue', label='Actifs')
        ax4.bar(x_pos + bar_width, passifs, width=bar_width, color='lightgreen', label='Passifs')
        ax4.set_title('Structure du bilan')
        ax4.set_ylabel('Millions DZD')
        ax4.set_xticks(x_pos + bar_width / 2)
        ax4.set_xticklabels(df.index)
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        canvas4 = FigureCanvas(fig4)
        self.graphs_container.addWidget(canvas4)

        # Graphique 5: Ratio de liquidité
        fig5 = Figure(figsize=(8, 4))
        ax5 = fig5.add_subplot(111)
        ax5.plot(df.index, df['Ratio_liquidite'], marker='o', color='purple', linewidth=2)
        ax5.axhline(y=1, color='r', linestyle='--', alpha=0.7)
        ax5.set_title('Ratio de liquidité générale')
        ax5.set_ylabel('Ratio')
        ax5.grid(True, alpha=0.3)
        canvas5 = FigureCanvas(fig5)
        self.graphs_container.addWidget(canvas5)

        # Graphique 6: Évolution de la trésorerie
        fig6 = Figure(figsize=(8, 4))
        ax6 = fig6.add_subplot(111)
        ax6.plot(df.index, df['Tresorerie'] / 1_000_000, marker='o', color='orange', linewidth=2)
        ax6.set_title('Évolution de la trésorerie')
        ax6.set_ylabel('Millions DZD')
        ax6.grid(True, alpha=0.3)
        canvas6 = FigureCanvas(fig6)
        self.graphs_container.addWidget(canvas6)

    def _export_pdf(self):
        """Exporte les résultats en PDF"""
        success, message = self.controller.export_controller.export_to_pdf("rapport_analyse.pdf")
        if success:
            QMessageBox.information(self, "Succès", message)
        else:
            QMessageBox.warning(self, "Erreur", message)