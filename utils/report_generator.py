from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile
import os


class ReportGenerator:
    @staticmethod
    def generate_pdf_report(data, output_path):
        pdf = FPDF()
        pdf.set_auto_page_break(True, 15)
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Rapport d\'Analyse Comptable', 0, 1, 'C')

        temp_dir = tempfile.mkdtemp()
        graph_path = os.path.join(temp_dir, 'ca_evolution.png')

        plt.figure(figsize=(8, 4))
        data['Chiffre_affaires'].plot(kind='bar')
        plt.title('Évolution du Chiffre d\'Affaires')
        plt.savefig(graph_path)
        plt.close()

        pdf.image(graph_path, x=10, y=30, w=180)
        pdf.output(output_path)
        return True