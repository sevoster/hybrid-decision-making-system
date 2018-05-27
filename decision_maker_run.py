import sys
import argparse

from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow


def parse_arguments():
    parser = argparse.ArgumentParser("Argument parser for decision system")

    parser.add_argument("-p", "--path",
                        help="Path to the file with decision graph to import",
                        type=str)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    app = QApplication([])
    main_window = MainWindow()

    if args.path:
        main_window.import_from_path(args.path)
        pass

    sys.exit(app.exec_())
