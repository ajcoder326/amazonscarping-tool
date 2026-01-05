"""
Amazon Traffic Simulator GUI Application
Simple interface for selecting ASIN file and cookies
"""
import sys
import json
import threading
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox,
    QTextEdit, QProgressBar, QSpinBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QIcon, QPixmap
import os

class OutputCapture:
    """Capture print output"""
    def __init__(self, callback):
        self.callback = callback
    
    def write(self, text):
        if text.strip():
            self.callback(text.strip())
    
    def flush(self):
        pass


class SimulatorWorker(QObject):
    """Worker thread for running simulator"""
    progress = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, asin_file, cookie_file, limit=None, delay=None):
        super().__init__()
        self.asin_file = asin_file
        self.cookie_file = cookie_file
        self.limit = limit
        self.delay = delay
    
    def run(self):
        try:
            self.progress.emit("🚀 Starting Amazon Traffic Simulator...")
            
            # Import pandas for reading files
            import pandas as pd
            
            # Read ASINs from file
            try:
                if self.asin_file.endswith('.xlsx') or self.asin_file.endswith('.xls'):
                    df = pd.read_excel(self.asin_file)
                elif self.asin_file.endswith('.csv'):
                    df = pd.read_csv(self.asin_file)
                else:
                    raise ValueError("File must be .xlsx, .xls, or .csv")
                
                # Find ASIN column
                asin_column = None
                for col in df.columns:
                    if 'asin' in col.lower():
                        asin_column = col
                        break
                
                if asin_column is None:
                    asin_column = df.columns[0]
                
                asins = df[asin_column].dropna().astype(str).tolist()
                self.progress.emit(f"✅ Loaded {len(asins)} ASINs")
            
            except Exception as e:
                self.error.emit(f"Error reading ASIN file: {str(e)}")
                self.finished.emit()
                return
            
            # Read cookies
            try:
                with open(self.cookie_file, 'r') as f:
                    cookie_data = json.load(f)
                
                if isinstance(cookie_data, dict) and 'cookies' in cookie_data:
                    cookies = cookie_data['cookies']
                elif isinstance(cookie_data, list):
                    cookies = cookie_data
                else:
                    raise ValueError("Invalid cookie format")
                
                self.progress.emit(f"🍪 Loaded {len(cookies)} cookies")
            
            except Exception as e:
                self.error.emit(f"Error reading cookie file: {str(e)}")
                self.finished.emit()
                return
            
            # Apply limit if specified
            if self.limit and self.limit > 0:
                asins = asins[:self.limit]
                self.progress.emit(f"🔹 Limited to first {self.limit} ASINs")
            
            # Import the simulator
            from traffic_simulator import run_simulator
            
            # Capture output
            old_stdout = sys.stdout
            sys.stdout = OutputCapture(self.progress.emit)
            
            try:
                # Run simulator
                run_simulator(asins, delay=self.delay, cookies=cookies)
                self.progress.emit("\n✅ Traffic simulation completed successfully!")
            
            finally:
                sys.stdout = old_stdout
            
            self.finished.emit()
        
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")
            self.finished.emit()


class TrafficSimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = None
        self.worker_thread = None
    
    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("Amazon Traffic Simulator")
        self.setGeometry(100, 100, 900, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🚀 Amazon Traffic Simulator")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # File selection group
        file_group = QGroupBox("📁 File Selection")
        file_layout = QFormLayout()
        
        # ASIN file selection
        asin_layout = QHBoxLayout()
        self.asin_file_input = QLineEdit()
        self.asin_file_input.setReadOnly(True)
        self.asin_file_input.setPlaceholderText("Select your Excel/CSV file with ASINs...")
        asin_browse_btn = QPushButton("Browse ASIN File")
        asin_browse_btn.clicked.connect(self.select_asin_file)
        asin_browse_btn.setStyleSheet("background-color: #007BFF; color: white; padding: 5px; border-radius: 3px;")
        asin_layout.addWidget(self.asin_file_input)
        asin_layout.addWidget(asin_browse_btn)
        file_layout.addRow("ASIN File (.xlsx, .csv):", asin_layout)
        
        # Cookie file selection
        cookie_layout = QHBoxLayout()
        self.cookie_file_input = QLineEdit()
        self.cookie_file_input.setReadOnly(True)
        self.cookie_file_input.setPlaceholderText("Select your cookies JSON file...")
        cookie_browse_btn = QPushButton("Browse Cookie File")
        cookie_browse_btn.clicked.connect(self.select_cookie_file)
        cookie_browse_btn.setStyleSheet("background-color: #007BFF; color: white; padding: 5px; border-radius: 3px;")
        cookie_layout.addWidget(self.cookie_file_input)
        cookie_layout.addWidget(cookie_browse_btn)
        file_layout.addRow("Cookie File (.json):", cookie_layout)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        # Settings group
        settings_group = QGroupBox("⚙️ Settings (Optional)")
        settings_layout = QFormLayout()
        
        # Limit spinner
        self.limit_spinbox = QSpinBox()
        self.limit_spinbox.setMinimum(0)
        self.limit_spinbox.setMaximum(10000)
        self.limit_spinbox.setValue(0)
        self.limit_spinbox.setToolTip("0 = All ASINs")
        settings_layout.addRow("Limit ASINs (0 = All):", self.limit_spinbox)
        
        # Delay spinner
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setMinimum(0)
        self.delay_spinbox.setMaximum(300)
        self.delay_spinbox.setValue(0)
        self.delay_spinbox.setToolTip("0 = Random 10-30 seconds")
        settings_layout.addRow("Delay Between ASINs (seconds):", self.delay_spinbox)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️  START SIMULATION")
        self.start_btn.setStyleSheet("background-color: #28a745; color: white; padding: 10px; font-weight: bold; border-radius: 5px; font-size: 12px;")
        self.start_btn.clicked.connect(self.start_simulation)
        self.start_btn.setMinimumHeight(40)
        
        self.clear_btn = QPushButton("🔄 Clear All")
        self.clear_btn.setStyleSheet("background-color: #6c757d; color: white; padding: 10px; border-radius: 5px;")
        self.clear_btn.clicked.connect(self.clear_all)
        
        buttons_layout.addWidget(self.start_btn)
        buttons_layout.addWidget(self.clear_btn)
        main_layout.addLayout(buttons_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #28a745;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Output/Log area
        log_label = QLabel("📋 Output Log:")
        log_font = QFont()
        log_font.setBold(True)
        log_label.setFont(log_font)
        main_layout.addWidget(log_label)
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: 'Courier New'; font-size: 9px; padding: 5px; border-radius: 3px;")
        self.output_text.setMinimumHeight(200)
        main_layout.addWidget(self.output_text)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def select_asin_file(self):
        """Open file dialog to select ASIN file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select ASIN File",
            "",
            "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*.*)"
        )
        if file_path:
            self.asin_file_input.setText(file_path)
            self.statusBar().showMessage(f"ASIN file selected: {Path(file_path).name}")
    
    def select_cookie_file(self):
        """Open file dialog to select cookie file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cookie File",
            "",
            "JSON Files (*.json);;All Files (*.*)"
        )
        if file_path:
            self.cookie_file_input.setText(file_path)
            self.statusBar().showMessage(f"Cookie file selected: {Path(file_path).name}")
    
    def validate_inputs(self):
        """Validate user inputs"""
        asin_file = self.asin_file_input.text().strip()
        cookie_file = self.cookie_file_input.text().strip()
        
        if not asin_file:
            QMessageBox.warning(self, "Missing Input", "Please select an ASIN file!")
            return False
        
        if not cookie_file:
            QMessageBox.warning(self, "Missing Input", "Please select a cookie file!")
            return False
        
        if not os.path.exists(asin_file):
            QMessageBox.error(self, "File Not Found", f"ASIN file not found: {asin_file}")
            return False
        
        if not os.path.exists(cookie_file):
            QMessageBox.error(self, "File Not Found", f"Cookie file not found: {cookie_file}")
            return False
        
        # Validate cookie file is valid JSON
        try:
            with open(cookie_file, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'cookies' not in data:
                    if not isinstance(data, list):
                        raise ValueError("Cookie file must be JSON array or have 'cookies' key")
        except json.JSONDecodeError:
            QMessageBox.error(self, "Invalid JSON", "Cookie file is not valid JSON!")
            return False
        except Exception as e:
            QMessageBox.error(self, "Cookie File Error", f"Error reading cookie file: {str(e)}")
            return False
        
        return True
    
    def start_simulation(self):
        """Start the traffic simulation"""
        if not self.validate_inputs():
            return
        
        if self.worker_thread and self.worker_thread.is_alive():
            QMessageBox.warning(self, "Already Running", "Simulation is already running!")
            return
        
        # Disable start button
        self.start_btn.setEnabled(False)
        self.start_btn.setText("⏳ RUNNING...")
        
        # Clear output
        self.output_text.clear()
        self.progress_bar.setValue(0)
        
        # Get inputs
        asin_file = self.asin_file_input.text()
        cookie_file = self.cookie_file_input.text()
        limit = self.limit_spinbox.value() if self.limit_spinbox.value() > 0 else None
        delay = self.delay_spinbox.value() if self.delay_spinbox.value() > 0 else None
        
        # Create worker
        self.worker = SimulatorWorker(asin_file, cookie_file, limit, delay)
        self.worker.progress.connect(self.append_output)
        self.worker.finished.connect(self.simulation_finished)
        self.worker.error.connect(self.simulation_error)
        
        # Run in thread
        self.worker_thread = threading.Thread(target=self.worker.run)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
        self.statusBar().showMessage("Simulation running...")
    
    def append_output(self, text):
        """Append text to output log"""
        self.output_text.append(text)
        # Auto-scroll to bottom
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )
        # Update progress (if log line contains step count)
        if "/" in text and "Processing ASIN:" in text:
            try:
                parts = text.split("[")[1].split("]")[0].split("/")
                current = int(parts[0])
                total = int(parts[1])
                progress = int((current / total) * 100)
                self.progress_bar.setValue(progress)
            except:
                pass
    
    def simulation_finished(self):
        """Called when simulation finishes"""
        self.start_btn.setEnabled(True)
        self.start_btn.setText("▶️  START SIMULATION")
        self.progress_bar.setValue(100)
        self.statusBar().showMessage("Simulation completed!")
        QMessageBox.information(self, "Complete", "Traffic simulation completed successfully!")
    
    def simulation_error(self, error_msg):
        """Called when simulator encounters error"""
        self.start_btn.setEnabled(True)
        self.start_btn.setText("▶️  START SIMULATION")
        self.statusBar().showMessage("Error occurred!")
        self.append_output(f"\n❌ {error_msg}")
        QMessageBox.critical(self, "Error", error_msg)
    
    def clear_all(self):
        """Clear all inputs and output"""
        self.asin_file_input.clear()
        self.cookie_file_input.clear()
        self.output_text.clear()
        self.progress_bar.setValue(0)
        self.limit_spinbox.setValue(0)
        self.delay_spinbox.setValue(0)
        self.statusBar().showMessage("Cleared all inputs")


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = TrafficSimulatorGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
