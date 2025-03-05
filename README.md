# Task Manager Application

A modern, feature-rich task management application built with Python and PyQt5, featuring a sleek dark theme and workspace management capabilities. Available both as source code and standalone executable.

## Features

- **Dark Theme**: Modern and eye-friendly dark interface
- **Workspace Management**: Create and manage multiple workspaces for different projects or contexts
- **Task Operations**:
  - Create new tasks with title and description
  - Edit existing tasks
  - Mark tasks as complete/incomplete
  - Delete tasks
  - Clear task form
- **Visual Task List**: Tree view displaying task ID, title, description, and status
- **Status Updates**: Visual feedback for all operations
- **Persistent Storage**: Tasks are saved automatically in JSON format

## Installation

### Option 1: Standalone Executable (Windows)

1. Download the latest release from the GitHub Releases page
2. Extract the ZIP file
3. Run `main.exe` - no installation or Python required

### Option 2: From Source Code

1. Ensure you have Python 3.x installed on your system
2. Clone this repository or download the source code
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```
   python main.py
   ```

2. The application window will open with two main sections:
   - Left: Task list and workspace management
   - Right: Task input form

### Managing Workspaces

- **Create Workspace**: 
  - Click "Create Workspace" button or use menu
  - Enter workspace name when prompted
  - New workspace will be created and activated

- **Switch Workspace**: 
  - Use the Workspaces menu
  - Select desired workspace from the list

- **Delete Workspace**: 
  - Click "Delete Workspace" button or use menu
  - Confirm deletion when prompted
  - Note: Default workspace cannot be deleted

### Managing Tasks

1. **Add Task**:
   - Enter task title (required)
   - Add optional description
   - Click "Add Task"

2. **Edit Task**:
   - Double-click any task in the list
   - Modify title/description
   - Click "Update Task"

3. **Complete/Uncomplete Task**:
   - Select task in the list
   - Click "Complete Task" or "Uncomplete Task"

4. **Delete Task**:
   - Select task in the list
   - Click "Delete Task"

5. **Clear Form**:
   - Click "Clear Form" to reset input fields

## Data Storage

Tasks are stored in JSON format:
- Location: `~/Documents/TaskManager/<workspace_name>/tasks.json`
- Each workspace has its own tasks file
- Data is saved automatically after each operation

## Technical Details

- Built with Python 3.x and PyQt5
- Uses QTreeWidget for task display
- Implements a modern dark theme using QPalette
- Features a responsive split-pane interface