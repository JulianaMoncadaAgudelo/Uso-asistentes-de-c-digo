# Employee and Contract Management System

A command-line application for managing employee records and labor contracts with persistent JSON storage. Built with Python, this system provides a complete CRUD interface for employee management, contract tracking, and reporting capabilities.

## Project Overview

This application demonstrates the implementation of a structured data management system with clean architecture principles. It allows users to maintain employee records, associate labor contracts with employees, track contract expiration dates, and generate reports through both an interactive menu and individual CLI commands.

## Features

- **Employee Management**: Create, read, update, and delete employee records
- **Contract Administration**: Associate labor contracts with employees, including start dates, end dates, and salary information
- **Data Validation**: Comprehensive input validation for dates, employee existence, and data integrity
- **Reporting**: Generate reports for expired contracts and identify employees with expired contracts
- **Interactive CLI**: User-friendly menu-driven interface with formatted table displays
- **JSON Persistence**: Reliable data storage and retrieval using JSON files
- **Comprehensive Testing**: Full test suite covering all core functionalities

## Tech Stack

- **Python 3.x**: Core programming language
- **Click**: Command-line interface creation and parsing
- **Rich**: Terminal formatting and styled output with tables
- **pytest**: Testing framework for unit and integration tests
- **JSON**: Data storage and serialization

## Project Structure

```
.
├── src/
│   └── employee_manager/
│       ├── __init__.py
│       ├── models.py              # Data models (Employee, Contract)
│       ├── json_storage.py        # JSON storage manager
│       ├── gestor_empleados.py    # Employee CRUD operations
│       ├── gestor_contratos.py    # Contract CRUD operations
│       ├── reportes.py            # Reporting and queries
│       ├── main.py                # Main CLI interface
│       └── cli.py                 # Alternative CLI interface
├── tests/                         # Unit test suite
│   ├── test_models.py
│   ├── test_json_storage.py
│   ├── test_gestor_empleados.py
│   ├── test_gestor_contratos.py
│   ├── test_reportes.py
│   ├── test_main_cli.py
│   └── test_main_menu.py
├── data/                          # JSON data storage
│   └── empleados.json
├── requirements.txt               # Project dependencies
└── README.md
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Uso-asistentes-de-c-digo
   ```

2. Create and activate a virtual environment:
   
   **On macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   
   **On Windows:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Upgrade pip and install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Usage

### Interactive Menu

Launch the interactive menu for the easiest way to use the application:

```bash
python -m employee_manager.main menu
```

The menu provides the following options:

1. Add employee
2. List all employees
3. Search employee by ID
4. Delete employee
5. Associate contract with employee
6. List expired contracts
7. Initialize database (reset)
0. Exit

### Command-Line Interface

Individual commands are also available for direct operations:

**Initialize the database:**
```bash
python -m employee_manager.main init-db
```

**List all employees:**
```bash
python -m employee_manager.main list-employees
```

### Usage Example

**Adding an employee and associating a contract:**

1. Run the interactive menu:
   ```bash
   python -m employee_manager.main menu
   ```

2. Select option `1` to add an employee:
   - Enter name: `John Smith`
   - Enter position: `Software Engineer`

3. Select option `5` to associate a contract:
   - Enter employee ID: `1`
   - Enter start date: `2024-01-15`
   - Enter end date: `2025-01-15`
   - Enter salary: `75000`

4. Select option `6` to view expired contracts and verify contract tracking

## Testing

The project includes a comprehensive test suite covering all main functionalities.

**Run all tests:**
```bash
pytest tests/ -v
```

**Run specific test module:**
```bash
pytest tests/test_gestor_empleados.py -v
```

**Run tests with coverage report:**
```bash
pytest tests/ --cov=employee_manager --cov-report=html
```

## Data Validation

The application implements robust validation mechanisms:

- Date format validation (YYYY-MM-DD)
- End date must be later than start date
- Employee existence verification before contract creation
- Prevention of duplicate IDs
- Protection against ID modification for existing records
- Empty field validation for required inputs
- Salary value validation (non-negative)

## Key Implementation Details

### Clean Architecture

The project follows separation of concerns with distinct modules for:
- Data models (dataclasses)
- Storage layer (JSON operations)
- Business logic (employee and contract management)
- Presentation layer (CLI interface)

### Error Handling

Comprehensive error handling with descriptive exception messages for:
- Invalid input data
- Non-existent records
- File system operations
- JSON parsing errors

### Code Quality

- **Naming conventions**: Consistent use of snake_case following PEP 8
- **Type hints**: Function signatures include type annotations
- **Documentation**: Docstrings for all public functions and classes
- **Modularity**: Reusable functions with single responsibility principle

## Future Improvements

- **Database Integration**: Migrate from JSON to SQLite or PostgreSQL for improved performance and scalability
- **Web Interface**: Develop a REST API with Flask or FastAPI and a frontend dashboard
- **User Authentication**: Implement role-based access control for multi-user environments
- **Advanced Reporting**: Add visualization capabilities with charts and graphs
- **Export Functionality**: Enable export to CSV and Excel formats
- **Email Notifications**: Automated alerts for upcoming contract expirations
- **Contract Templates**: Predefined contract templates for different employee types
- **Audit Logging**: Track all changes with timestamps and user information
- **Search Enhancement**: Full-text search and filtering capabilities
- **Data Validation**: Integration with external validation services for email and contact information

## Contributing

Contributions are welcome. Please follow the existing code style and ensure all tests pass before submitting pull requests.

## License

This project is available for educational and portfolio purposes.

---

**Developed as part of a software development learning project demonstrating Python programming, CLI design, testing practices, and clean code principles.**
