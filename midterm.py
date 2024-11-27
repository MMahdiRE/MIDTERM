import sys
import os
import json
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QPushButton, QTextEdit, QLabel, QVBoxLayout, QWidget
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Analyzer")
        self.setGeometry(100, 100, 800, 600)

        # Layout and widgets
        layout = QVBoxLayout()

        self.input_label = QLabel("Enter input file path:")
        layout.addWidget(self.input_label)

        self.input_file = QLineEdit()
        layout.addWidget(self.input_file)

        self.output_label = QLabel("Enter output file path:")
        layout.addWidget(self.output_label)

        self.output_file = QLineEdit()
        layout.addWidget(self.output_file)

        self.ignored_label = QLabel("Enter ignored words file path (optional):")
        layout.addWidget(self.ignored_label)

        self.ignored_file = QLineEdit()
        layout.addWidget(self.ignored_file)

        self.analyze_button = QPushButton("Analyze File")
        layout.addWidget(self.analyze_button)

        self.result_label = QLabel("Analysis Results:")
        layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        # Central widget setup
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Connect button to function
        self.analyze_button.clicked.connect(self.analyze_file)

    def analyze_file(self):
        input_file = self.input_file.text().strip()
        output_file = self.output_file.text().strip()
        ignored_words_file = self.ignored_file.text().strip() or None

        try:
            if not os.path.exists(input_file):
                self.result_text.setText(f"Error: The file '{input_file}' does not exist.")
                return

            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()

            ignored_words = set()
            if ignored_words_file and os.path.exists(ignored_words_file):
                with open(ignored_words_file, 'r', encoding='utf-8') as file:
                    ignored_words = set(file.read().split())

            words = re.findall(r'\b\w+\b', text.lower())
            filtered_words = [word for word in words if word not in ignored_words]

            word_counts = {}
            for word in filtered_words:
                word_counts[word] = word_counts.get(word, 0) + 1

            line_count = text.count('\n') + 1
            sentence_count = len(re.split(r'[.!?]', text)) - 1
            word_count = len(filtered_words)
            longest_words = sorted(set(filtered_words), key=len, reverse=True)[:5]
            avg_word_length = sum(len(word) for word in filtered_words) / len(filtered_words) if filtered_words else 0

            result = {
                "line_count": line_count,
                "sentence_count": sentence_count,
                "word_count": word_count,
                "word_occurrences": word_counts,
                "longest_words": longest_words,
                "average_word_length": avg_word_length
            }

            # Save result to output file
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(result, file, indent=4)

            # Display result in text area
            result_text = f"""
Line Count: {line_count}
Sentence Count: {sentence_count}
Word Count: {word_count}
Longest Words: {', '.join(longest_words)}
Average Word Length: {avg_word_length:.2f}

Word Occurrences:
{json.dumps(word_counts, indent=4)}
"""
            self.result_text.setText(result_text)

        except Exception as e:
            self.result_text.setText(f"Error: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
