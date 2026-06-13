import sys
import math
import re
from PyQt5.QtWidgets import QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel
)


from matplotlib.pyplot import title
from pyparsing import line
from qfluentwidgets import (
    CardWidget,
    PasswordLineEdit,
    ProgressBar,
    StrongBodyLabel,
    SubtitleLabel,
    setTheme,
    Theme
)


class PasswordAnalyzer(QWidget):

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # Header Layout
        header = QHBoxLayout()

        # Logo
        logo = QLabel()
        logo.setPixmap(
            QPixmap("lock1.png").scaled(
                40, 40,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        # Title
        title = SubtitleLabel("Password Strength Analyzer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: white;
            padding: 10px;
        """)

        header.addStretch()
        header.addWidget(logo)
        header.addSpacing(10)
        header.addWidget(title)
        header.addStretch()

        # Blue line
        line = QLabel()
        line.setFixedHeight(3)
        line.setStyleSheet("""
            background-color: #00D4FF;
            border-radius: 2px;
        """)

        # Add AFTER creating them
        main_layout.addLayout(header)
        main_layout.addWidget(line)


       

        # Card
        card = CardWidget()
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(15)
        card.setStyleSheet("""
        CardWidget {
        background-color: #1E1E1E;
        border: 2px solid #00D4FF;
        border-radius: 20px;
        }

        QLabel {
         background: transparent;
        }
        """)

        # Password Field
        self.password_box = PasswordLineEdit()
        self.password_box.setPlaceholderText("Enter your password")

        # Progress Bar
        self.progress = ProgressBar()
        self.progress.setFixedHeight(24)
        self.progress.setValue(0)

        # Animation
        self.animation = QPropertyAnimation(
            self.progress,
            b"value"
        )
        self.animation.setDuration(400)

        # Percentage
        self.percent_label = StrongBodyLabel("0%")
        self.percent_label.setAlignment(Qt.AlignCenter)
        self.percent_label.setStyleSheet("""
                color:white;
            font-size: 24px;
            font-weight: 700;
        """)

        # Strength Label
        self.strength_label = StrongBodyLabel("Start typing...")
        self.strength_label.setAlignment(Qt.AlignCenter)
        self.strength_label.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
        """)

        # Requirements
        req_title = StrongBodyLabel("Security Requirements")
        req_title.setStyleSheet("""
         color:white;
        font-size:18px;
        font-weight:700;
        """)

        self.length_check = QLabel("✗ Minimum 8 Characters")
        self.upper_check = QLabel("✗ Uppercase Letter")
        self.lower_check = QLabel("✗ Lowercase Letter")
        self.number_check = QLabel("✗ Number")
        self.special_check = QLabel("✗ Special Character")

        # Statistics
        stats_title = StrongBodyLabel("Password Statistics")
        stats_title.setStyleSheet("""
        color:white;
        font-size:18px;
        font-weight:700;
        """)

        self.length_label = QLabel("Length: 0")
        self.length_label.setStyleSheet("color:white;")

        self.entropy_label = QLabel("Entropy: 0 bits")
        self.entropy_label.setStyleSheet("color:white;")

        self.crack_time_label = QLabel("Estimated Crack Time: Instantly")
        self.crack_time_label.setStyleSheet("color:white;")

        card_layout.addWidget(self.password_box)
        card_layout.addWidget(self.progress)
        card_layout.addWidget(self.percent_label)
        card_layout.addWidget(self.strength_label)

        card_layout.addSpacing(10)

        card_layout.addWidget(req_title)
        card_layout.addWidget(self.length_check)
        card_layout.addWidget(self.upper_check)
        card_layout.addWidget(self.lower_check)
        card_layout.addWidget(self.number_check)
        card_layout.addWidget(self.special_check)

        card_layout.addSpacing(10)

        card_layout.addWidget(stats_title)
        card_layout.addWidget(self.length_label)
        card_layout.addWidget(self.entropy_label)
        card_layout.addWidget(self.crack_time_label)

        main_layout.addWidget(title)
        main_layout.addWidget(card)

        self.password_box.textChanged.connect(
            self.analyze_password
        )

    def set_check_style(self, label, ok):

        if ok:
            label.setStyleSheet("""
                color:#52c41a;
                font-size:14px;
                font-weight:600;
            """)
        else:
            label.setStyleSheet("""
                color:#ff4d4f;
                font-size:14px;
                font-weight:600;
            """)

    def calculate_entropy(self, password):

        pool = 0

        if re.search(r"[a-z]", password):
            pool += 26

        if re.search(r"[A-Z]", password):
            pool += 26

        if re.search(r"\d", password):
            pool += 10

        if re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            password
        ):
            pool += 32

        if pool == 0:
            return 0

        return round(
            len(password) * math.log2(pool)
        )

    def crack_time(self, entropy):

        if entropy < 30:
            return "Instantly"

        elif entropy < 45:
            return "Few Hours"

        elif entropy < 60:
            return "Few Months"

        elif entropy < 75:
            return "Several Years"

        else:
            return "Centuries"

    def analyze_password(self):

        password = self.password_box.text()

        score = 0

        length_ok = len(password) >= 8
        upper_ok = bool(
            re.search(r"[A-Z]", password)
        )
        lower_ok = bool(
            re.search(r"[a-z]", password)
        )
        number_ok = bool(
            re.search(r"\d", password)
        )
        special_ok = bool(
            re.search(
                r"[!@#$%^&*(),.?\":{}|<>]",
                password
            )
        )

        if length_ok:
            score += 20

        if upper_ok:
            score += 20

        if lower_ok:
            score += 20

        if number_ok:
            score += 20

        if special_ok:
            score += 20

        current = self.progress.value()

        self.animation.stop()
        self.animation.setStartValue(current)
        self.animation.setEndValue(score)
        self.animation.start()

        self.percent_label.setText(f"{score}%")

        self.length_check.setText(
            f"{'✓' if length_ok else '✗'} Minimum 8 Characters"
        )

        self.upper_check.setText(
            f"{'✓' if upper_ok else '✗'} Uppercase Letter"
        )

        self.lower_check.setText(
            f"{'✓' if lower_ok else '✗'} Lowercase Letter"
        )

        self.number_check.setText(
            f"{'✓' if number_ok else '✗'} Number"
        )

        self.special_check.setText(
            f"{'✓' if special_ok else '✗'} Special Character"
        )

        self.set_check_style(self.length_check, length_ok)
        self.set_check_style(self.upper_check, upper_ok)
        self.set_check_style(self.lower_check, lower_ok)
        self.set_check_style(self.number_check, number_ok)
        self.set_check_style(self.special_check, special_ok)

        if score <= 40:

            self.strength_label.setText("Weak Password")
            self.strength_label.setStyleSheet("""
                color:#ff4d4f;
                font-size:28px;
                font-weight:700;
            """)

        elif score <= 80:

            self.strength_label.setText("Medium Password")
            self.strength_label.setStyleSheet("""
                color:#faad14;
                font-size:28px;
                font-weight:700;
            """)

        else:

            self.strength_label.setText("Strong Password")
            self.strength_label.setStyleSheet("""
                color:#52c41a;
                font-size:28px;
                font-weight:700;
            """)

        entropy = self.calculate_entropy(password)

        self.length_label.setText(
            f"Length: {len(password)}"
        )

        self.entropy_label.setText(
            f"Entropy: {entropy} bits"
        )

        self.crack_time_label.setText(
            f"Estimated Crack Time: {self.crack_time(entropy)}"
        )


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("lock.png"))

        self.setWindowTitle(
            "Password Strength Analyzer"
        )

        self.resize(400, 700)

        self.setStyleSheet("""
        QMainWindow {
         background-color: #121212;
        }
        """)

        self.setCentralWidget(
            PasswordAnalyzer()
        )


if __name__ == "__main__":

    app = QApplication(sys.argv)

    setTheme(Theme.DARK)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
