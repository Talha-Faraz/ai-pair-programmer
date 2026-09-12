import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QTextEdit, QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor

from modules.capture_engine import WindowCapturer
from modules.ai_analyzer import AIPairProgrammer

class AIWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, capturer, analyzer, target_window, user_query):
        super().__init__()
        self.capturer = capturer
        self.analyzer = analyzer
        self.target_window = target_window
        self.user_query = user_query

    def run(self):
        try:
            image_path = self.capturer.capture_target_window(self.target_window)
            if "Error" in image_path:
                self.error.emit(image_path)
                return
            result = self.analyzer.analyze_code_screenshot(image_path, self.user_query)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(f"Process failed: {str(e)}")

class FloatingAIAssistant(QWidget):
    def __init__(self):
        super().__init__()
        
        # MAGIC FIX FOR MAC FULLSCREEN: 'Qt.WindowType.Tool'
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool 
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.capturer = WindowCapturer()
        try:
            self.analyzer = AIPairProgrammer()
        except ValueError as e:
            print(f"Startup Error: {e}")
            sys.exit(1)
            
        self.is_expanded = False
        self.dragPos = None
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10) # Drop shadow ke liye thodi space
        
        # --- Main Chat Container (Rounded + Shadow) ---
        self.chat_container = QFrame()
        self.chat_container.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e; /* VS Code Dark Background */
                border-radius: 12px;
                border: 1px solid #333333;
            }
            QLabel { color: #cccccc; font-family: 'SF Pro Display', sans-serif; }
        """)
        
        # Drop Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.chat_container.setGraphicsEffect(shadow)
        
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(15, 15, 15, 15)
        
        # --- Sleek Drag Handle ---
        self.drag_handle = QLabel("•••  AI Pair Programmer  •••")
        self.drag_handle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_handle.setStyleSheet("""
            background-color: transparent; 
            color: #666666; 
            font-size: 11px; 
            font-weight: bold;
            border: none;
            padding-bottom: 5px;
        """)
        
        # --- Top Bar ---
        top_bar = QHBoxLayout()
        self.window_selector = QComboBox()
        self.window_selector.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d; 
                color: #cccccc;
                padding: 6px; 
                border-radius: 6px;
                border: 1px solid #3c3c3c;
            }
            QComboBox::drop-down { border: none; }
        """)
        self.refresh_windows()
        
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(30, 30)
        refresh_btn.setStyleSheet("background-color: #2d2d2d; border-radius: 6px; border: 1px solid #3c3c3c; font-size: 14px;")
        refresh_btn.clicked.connect(self.refresh_windows)
        
        top_bar.addWidget(self.window_selector)
        top_bar.addWidget(refresh_btn)
        
        # --- Chat Display (Colored Text Support) ---
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e; 
                color: #d4d4d4;
                border: none; 
                font-family: 'Menlo', monospace; 
                font-size: 13px;
                padding-top: 10px;
            }
        """)
        self.chat_display.setHtml("<span style='color:#858585;'>// System: Ready. Select IDE and ask away...</span><br>")
        
        # --- Chat Input Area ---
        input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Ask AI to find errors or optimize...")
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background-color: #2d2d2d; 
                color: white; 
                padding: 10px; 
                border-radius: 8px;
                border: 1px solid #3c3c3c;
            }
            QLineEdit:focus { border: 1px solid #007fd4; }
        """)
        self.chat_input.returnPressed.connect(self.run_analysis)
        
        self.send_btn = QPushButton("Check")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #007fd4; 
                color: white; 
                padding: 10px 15px; 
                border-radius: 8px; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #006eb8; }
            QPushButton:disabled { background-color: #4d4d4d; color: #888888; }
        """)
        self.send_btn.clicked.connect(self.run_analysis)
        
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(self.send_btn)
        
        # Adding to Chat Layout
        chat_layout.addWidget(self.drag_handle)
        chat_layout.addLayout(top_bar)
        chat_layout.addWidget(self.chat_display)
        chat_layout.addLayout(input_layout)
        
        self.chat_container.setLayout(chat_layout)
        self.chat_container.hide()
        
        # --- Floating Icon (More subtle and modern) ---
        self.icon_btn = QPushButton("✨")
        self.icon_btn.setFixedSize(50, 50)
        self.icon_btn.setStyleSheet("""
            QPushButton { 
                border-radius: 25px; 
                background-color: #007fd4; 
                color: white; 
                font-size: 24px; 
                border: 2px solid #1e1e1e;
            }
            QPushButton:hover { background-color: #006eb8; }
        """)
        
        icon_shadow = QGraphicsDropShadowEffect(self)
        icon_shadow.setBlurRadius(15)
        icon_shadow.setXOffset(0)
        icon_shadow.setYOffset(4)
        icon_shadow.setColor(QColor(0, 0, 0, 100))
        self.icon_btn.setGraphicsEffect(icon_shadow)
        
        self.icon_btn.clicked.connect(self.toggle_interface)
        
        self.main_layout.addWidget(self.chat_container)
        self.main_layout.addWidget(self.icon_btn, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.setLayout(self.main_layout)
        self.resize(70, 70)

    # --- DRAGGING LOGIC ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragPos is not None:
            delta = event.globalPosition().toPoint() - self.dragPos
            self.move(self.pos() + delta)
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragPos = None
    # ----------------------

    def refresh_windows(self):
        self.window_selector.clear()
        windows = self.capturer.get_open_windows()
        if windows:
            self.window_selector.addItems(windows)
        else:
            self.window_selector.addItem("No active windows found")

    def toggle_interface(self):
        if self.is_expanded:
            self.chat_container.hide()
            self.resize(70, 70)
        else:
            self.refresh_windows()
            self.chat_container.show()
            self.resize(420, 600)
        self.is_expanded = not self.is_expanded

    def append_chat(self, sender, text, color):
        """Helper to style chat messages with colors"""
        formatted_text = f"<span style='color:{color}; font-weight:bold;'>{sender}</span><br><span style='color:#cccccc;'>{text}</span><br><br>"
        self.chat_display.append(formatted_text)
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())

    def run_analysis(self):
        target = self.window_selector.currentText()
        if not target or target == "No active windows found":
            self.append_chat("⚠️ System", "Please select a valid window from the dropdown.", "#f48771")
            return

        user_text = self.chat_input.text().strip()
        self.chat_input.clear()
        
        if user_text:
            self.append_chat("👤 You:", user_text, "#569cd6") # VS Code Blue
            query = user_text
        else:
            query = "Check this screen for any syntax errors, bugs, or improvements."
            self.append_chat("🔍 System:", f"Capturing '{target}' for auto-analysis...", "#c586c0") # VS Code Purple
            
        self.send_btn.setEnabled(False)
        self.send_btn.setText("...")
        
        self.worker = AIWorker(self.capturer, self.analyzer, target, query)
        self.worker.finished.connect(self.on_analysis_complete)
        self.worker.error.connect(self.on_analysis_error)
        self.worker.start()

    def on_analysis_complete(self, result):
        # Format the AI output text to handle basic newlines in HTML
        html_result = result.replace('\n', '<br>')
        self.append_chat("✨ AI Pair Programmer:", html_result, "#4ec9b0") # VS Code Green
        self.reset_button()

    def on_analysis_error(self, error_msg):
        self.append_chat("❌ Error:", error_msg, "#f14c4c") # VS Code Red
        self.reset_button()
        
    def reset_button(self):
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Check")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FloatingAIAssistant()
    ex.show()
    sys.exit(app.exec())