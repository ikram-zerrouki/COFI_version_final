from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt


class DataTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def update_data(self):
        raw_data = self.controller.get_raw_data()
        if not raw_data:
            return

        years = sorted(raw_data.keys())
        metrics = list(raw_data[years[0]].keys())

        self.table.setRowCount(len(metrics))
        self.table.setColumnCount(len(years))
        self.table.setHorizontalHeaderLabels([f"Année {year}" for year in years])
        self.table.setVerticalHeaderLabels([m.replace('_', ' ').title() for m in metrics])

        for col, year in enumerate(years):
            for row, metric in enumerate(metrics):
                value = raw_data[year][metric]
                item = QTableWidgetItem(f"{value:,.2f}" if isinstance(value, (int, float)) else str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row, col, item)