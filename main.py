import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QLineEdit, QPushButton,
                           QTreeWidget, QTreeWidgetItem, QMessageBox,
                           QInputDialog, QMenu, QMenuBar, QFrame, QSplitter,
                           QStyle, QStyleFactory, QTextEdit)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QColor, QFont

class TodoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.workspace_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'TaskManager')
        self.current_workspace = 'default'
        self.ensure_workspace_exists()
        self.data_file = self.get_workspace_file()
        self.load_tasks()

        # Set dark theme
        self.setStyle(QStyleFactory.create('Fusion'))
        self.setup_dark_theme()

        # Window setup
        self.setWindowTitle('Task Manager')
        self.setMinimumSize(1600, 800)

        # Create menu bar
        self.create_menu_bar()

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panes
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Left pane: Task list
        task_widget = QWidget()
        task_layout = QVBoxLayout(task_widget)
        task_layout.setContentsMargins(20, 20, 20, 20)
        task_layout.setSpacing(10)

        # Workspace management buttons
        workspace_frame = QFrame()
        workspace_layout = QHBoxLayout(workspace_frame)
        workspace_layout.setContentsMargins(0, 0, 0, 10)

        create_workspace_btn = QPushButton('Create Workspace')
        create_workspace_btn.clicked.connect(self.create_workspace)
        create_workspace_btn.setStyleSheet(self.get_button_style())
        workspace_layout.addWidget(create_workspace_btn)

        delete_workspace_btn = QPushButton('Delete Workspace')
        delete_workspace_btn.clicked.connect(self.delete_workspace)
        delete_workspace_btn.setStyleSheet(self.get_button_style())
        workspace_layout.addWidget(delete_workspace_btn)

        task_layout.addWidget(workspace_frame)

        # Task tree widget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['ID', 'Title', 'Description', 'Status'])
        self.tree.setColumnWidth(0, 50)
        self.tree.setColumnWidth(1, 200)
        self.tree.setColumnWidth(2, 300)
        self.tree.setColumnWidth(3, 100)
        self.tree.itemDoubleClicked.connect(self.edit_task)
        self.tree.itemSelectionChanged.connect(self.on_task_selection_changed)
        self.tree.setStyleSheet(self.get_tree_style())
        task_layout.addWidget(self.tree)

        # Right pane: Task details
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(15)

        # Title input
        title_label = QLabel('Title:')
        title_label.setFont(QFont('Segoe UI', 10))
        self.title_entry = QLineEdit()
        self.title_entry.setStyleSheet(self.get_input_style())
        form_layout.addWidget(title_label)
        form_layout.addWidget(self.title_entry)

        # Description input
        desc_label = QLabel('Description:')
        desc_label.setFont(QFont('Segoe UI', 10))
        self.desc_entry = QTextEdit()
        self.desc_entry.setStyleSheet(self.get_input_style())
        self.desc_entry.setMinimumHeight(100)
        form_layout.addWidget(desc_label)
        form_layout.addWidget(self.desc_entry)

        # Buttons
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(10)

        self.add_button = QPushButton('Add Task')
        self.add_button.clicked.connect(self.add_task)
        self.add_button.setStyleSheet(self.get_button_style('primary'))
        button_layout.addWidget(self.add_button)

        self.complete_button = QPushButton('Complete Task')
        self.complete_button.clicked.connect(self.complete_task)
        self.complete_button.setStyleSheet(self.get_button_style())
        button_layout.addWidget(self.complete_button)

        delete_button = QPushButton('Delete Task')
        delete_button.clicked.connect(self.delete_task)
        delete_button.setStyleSheet(self.get_button_style('danger'))
        button_layout.addWidget(delete_button)

        clear_button = QPushButton('Clear Form')
        clear_button.clicked.connect(self.clear_form)
        clear_button.setStyleSheet(self.get_button_style())
        button_layout.addWidget(clear_button)

        form_layout.addWidget(button_frame)

        # Status label
        self.status_label = QLabel('')
        self.status_label.setStyleSheet('color: #4CAF50;')
        form_layout.addWidget(self.status_label)

        form_layout.addStretch()

        # Add widgets to splitter
        splitter.addWidget(task_widget)
        splitter.addWidget(form_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        self.refresh_task_list()

    def setup_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.WindowText, QColor(245, 245, 245))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(245, 245, 245))
        dark_palette.setColor(QPalette.ToolTipText, QColor(245, 245, 245))
        dark_palette.setColor(QPalette.Text, QColor(245, 245, 245))
        dark_palette.setColor(QPalette.Button, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ButtonText, QColor(245, 245, 245))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 50, 50))
        dark_palette.setColor(QPalette.Link, QColor(66, 155, 248))
        dark_palette.setColor(QPalette.Highlight, QColor(66, 155, 248))
        dark_palette.setColor(QPalette.HighlightedText, QColor(245, 245, 245))
        self.setPalette(dark_palette)

    def get_button_style(self, button_type='default'):
        base_style = '''
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }
            QPushButton:hover {
                background-color: %s;
            }
        '''

        if button_type == 'primary':
            return base_style % '#2196F3' + 'QPushButton { background-color: #1976D2; color: white; }'
        elif button_type == 'danger':
            return base_style % '#F44336' + 'QPushButton { background-color: #D32F2F; color: white; }'
        else:
            return base_style % '#424242' + 'QPushButton { background-color: #333333; color: white; }'

    def get_input_style(self):
        return '''
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #424242;
                border-radius: 4px;
                background-color: #2A2A2A;
                color: white;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #2196F3;
            }
        '''

    def get_tree_style(self):
        return '''
            QTreeWidget {
                background-color: #2A2A2A;
                border: 1px solid #424242;
                border-radius: 4px;
                color: #FFFFFF;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QTreeWidget::item {
                padding: 5px;
                color: #FFFFFF;
            }
            QTreeWidget::item:selected {
                background-color: #2196F3;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #333333;
                padding: 5px;
                border: 1px solid #424242;
                font-weight: bold;
                color: #FFFFFF;
            }
        '''

    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet('''
            QMenuBar {
                background-color: #333333;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #2196F3;
            }
        ''')
        self.workspace_menu = menubar.addMenu('Workspaces')
        self.workspace_menu.setStyleSheet('''
            QMenu {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #424242;
            }
            QMenu::item:selected {
                background-color: #2196F3;
            }
        ''')

        new_workspace_action = self.workspace_menu.addAction('New Workspace...')
        new_workspace_action.triggered.connect(self.create_workspace)

        delete_workspace_action = self.workspace_menu.addAction('Delete Workspace')
        delete_workspace_action.triggered.connect(self.delete_workspace)

        self.workspace_menu.addSeparator()
        self.update_workspace_menu(self.workspace_menu)

    def ensure_workspace_exists(self):
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)
        workspace_path = os.path.join(self.workspace_dir, self.current_workspace)
        if not os.path.exists(workspace_path):
            os.makedirs(workspace_path)

    def get_workspace_file(self):
        return os.path.join(self.workspace_dir, self.current_workspace, 'tasks.json')

    def create_workspace(self):
        workspace_name, ok = QInputDialog.getText(
            self, 'New Workspace', 'Enter workspace name:')
        if ok and workspace_name:
            self.current_workspace = workspace_name
            self.ensure_workspace_exists()
            self.data_file = self.get_workspace_file()
            self.tasks = []
            self.save_tasks()
            self.refresh_task_list()
            self.update_workspace_menu(self.workspace_menu)
            self.show_status(f'Created workspace: {workspace_name}')

    def switch_workspace(self, workspace):
        self.current_workspace = workspace
        self.data_file = self.get_workspace_file()
        self.load_tasks()
        self.refresh_task_list()
        self.show_status(f'Switched to workspace: {workspace}')

    def update_workspace_menu(self, menu):
        menu.clear()
        menu.addAction('New Workspace...').triggered.connect(self.create_workspace)
        menu.addAction('Delete Workspace').triggered.connect(self.delete_workspace)
        menu.addSeparator()

        workspaces = [d for d in os.listdir(self.workspace_dir)
                     if os.path.isdir(os.path.join(self.workspace_dir, d))]
        for workspace in workspaces:
            action = menu.addAction(workspace)
            action.triggered.connect(
                lambda checked, w=workspace: self.switch_workspace(w))

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.tasks = json.load(f)
            except:
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def refresh_task_list(self):
        self.tree.clear()
        for task in self.tasks:
            item = QTreeWidgetItem()
            item.setText(0, str(task['id']))
            item.setText(1, task['title'])
            item.setText(2, task['description'])
            item.setText(3, '✓ Completed' if task['completed'] else 'Pending')
            if task['completed']:
                item.setForeground(3, QColor('#4CAF50'))
            self.tree.addTopLevelItem(item)

    def clear_form(self):
        self.title_entry.clear()
        self.desc_entry.clear()
        self.status_label.clear()
        if hasattr(self, 'editing_task_id'):
            delattr(self, 'editing_task_id')
            self.add_button.setText('Add Task')

    def edit_task(self, item):
        task_id = int(item.text(0))
        task = next((task for task in self.tasks if task['id'] == task_id), None)

        if task:
            self.editing_task_id = task_id
            self.title_entry.setText(task['title'])
            self.desc_entry.setText(task.get('description', ''))
            self.add_button.setText('Update Task')
            self.show_status('Editing task...')

    def show_status(self, message, is_error=False):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            f"color: {'#F44336' if is_error else '#4CAF50'};")
        QApplication.processEvents()

    def add_task(self):
        title = self.title_entry.text().strip()
        description = self.desc_entry.toPlainText().strip()

        if not title:
            self.show_status('Title is required!', True)
            return

        if hasattr(self, 'editing_task_id'):
            # Update existing task
            for task in self.tasks:
                if task['id'] == self.editing_task_id:
                    task['title'] = title
                    task['description'] = description
            delattr(self, 'editing_task_id')
            self.add_button.setText('Add Task')
            success_message = 'Task updated successfully!'
        else:
            # Add new task
            task = {
                'id': len(self.tasks) + 1,
                'title': title,
                'description': description,
                'created_at': datetime.now().isoformat(),
                'completed': False
            }
            self.tasks.append(task)
            success_message = 'Task added successfully!'

        self.save_tasks()
        self.refresh_task_list()
        self.clear_form()
        self.show_status(success_message)

    def complete_task(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            self.show_status('Please select a task to complete!', True)
            return

        task_id = int(selected_items[0].text(0))
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']  # Toggle the completion status
                self.save_tasks()
                self.refresh_task_list()
                status_message = 'Task marked as pending!' if not task['completed'] else 'Task marked as complete!'
                # Update the button text based on task status
                self.complete_button.setText('Complete Task' if not task['completed'] else 'Uncomplete Task')
                self.show_status(status_message)
                return

    def delete_task(self):
        selected_items = self.tree.selectedItems()
        if not selected_items:
            self.show_status('Please select a task to delete!', True)
            return

        task_id = int(selected_items[0].text(0))
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.save_tasks()
        self.refresh_task_list()
        self.show_status('Task deleted successfully!')

    def delete_workspace(self):
        if self.current_workspace == 'default':
            self.show_status('Cannot delete default workspace!', True)
            return

        reply = QMessageBox.question(
            self, 'Delete Workspace',
            f'Are you sure you want to delete workspace "{self.current_workspace}"?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            workspace_path = os.path.join(self.workspace_dir, self.current_workspace)
            if os.path.exists(workspace_path):
                import shutil
                shutil.rmtree(workspace_path)

            self.current_workspace = 'default'
            self.data_file = self.get_workspace_file()
            self.load_tasks()
            self.refresh_task_list()
            self.update_workspace_menu(self.workspace_menu)
            self.show_status(f'Workspace {self.current_workspace} deleted successfully!')

    def on_task_selection_changed(self):
        selected_items = self.tree.selectedItems()
        if selected_items:
            task_id = int(selected_items[0].text(0))
            task = next((task for task in self.tasks if task['id'] == task_id), None)
            if task:
                self.complete_button.setText('Uncomplete Task' if task['completed'] else 'Complete Task')
        else:
            self.complete_button.setText('Complete Task')

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())