from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HomeTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Analyse Comptable")
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        desc = QLabel("Importez un fichier Excel pour analyser les données comptables")
        desc.setAlignment(Qt.AlignCenter)

        import_btn = QPushButton("Importer un fichier Excel")
        import_btn.setFixedSize(200, 40)
        import_btn.clicked.connect(self._import_file)

        layout.addStretch(1)
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addSpacing(30)
        layout.addWidget(import_btn, 0, Qt.AlignCenter)
        layout.addStretch(1)
        self.setLayout(layout)

    def _import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir un fichier Excel", "", "Fichiers Excel (*.xlsx *.xls)"
        )
        if file_path:
            success, message = self.controller.file_controller.load_excel_file(file_path)
            if not success:
                QMessageBox.critical(self, "Erreur", message)