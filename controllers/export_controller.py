from PyQt5.QtCore import QObject
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os


class ExportController(QObject):
    def __init__(self, main_controller):
        super().__init__()
        self.main_controller = main_controller

    def export_to_pdf(self, output_path):
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(True, 15)
            self._add_title(pdf)
            self._add_data_section(pdf)
            self._add_results_section(pdf)
            self._add_graphs_section(pdf)
            pdf.output(output_path)
            return True, "Export PDF réussi"
        except Exception as e:
            return False, f"Erreur d'export: {str(e)}"

    def _add_title(self, pdf):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Rapport d\'Analyse Comptable', 0, 1, 'C')
        pdf.ln(10)

    def _add_data_section(self, pdf):
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Données Extraites', 0, 1)
        pdf.set_font('Arial', '', 10)

        for year, data in self.main_controller.get_raw_data().items():
            pdf.cell(0, 10, f'Année {year}', 0, 1)
            for key, value in data.items():
                pdf.cell(50, 6, key.replace('_', ' '), 0, 0)
                pdf.cell(0, 6, f'{value:,.2f}', 0, 1)
            pdf.ln(5)

    def _add_results_section(self, pdf):
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Résultats Calculés', 0, 1)

        df = self.main_controller.get_processed_data()
        for col in df.columns:
            pdf.cell(60, 6, col.replace('_', ' '), 0, 0)
            pdf.cell(0, 6, f'{df[col].iloc[-1]:,.2f}', 0, 1)

    def _add_graphs_section(self, pdf):
        temp_dir = tempfile.mkdtemp()
        graph_path = os.path.join(temp_dir, 'graph.png')

        df = self.main_controller.get_processed_data()
        plt.figure(figsize=(8, 5))
        df['Chiffre_affaires'].plot(kind='bar')
        plt.title('Évolution du Chiffre d\'Affaires')
        plt.savefig(graph_path)
        plt.close()

        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Graphiques', 0, 1)
        pdf.image(graph_path, x=10, y=20, w=180)