# GCode Processing and Analysis Tool

This project is a web-based application designed to handle G-code files, primarily used in 3D printing and CNC machining. The application provides functionalities for uploading G-code files, parsing them, and storing relevant information in a database.

## Features

- **File Upload:** Users can upload G-code files through a web interface. The files are stored in a designated `uploads` directory on the server.

- **G-code Parsing:** Upon uploading, the application parses the G-code file to extract key information, such as movement commands and coordinates.

- **Database Integration:** Extracted data from the G-code files, including file name, file path, and other metadata, are stored in a SQLite database. This allows for efficient management and retrieval of file information.

- **Basic Web Interface:** The application includes a simple yet functional web interface with features like a title bar, left-hand navigation, and a footer. Users can navigate through the application, upload files, and view a list of uploaded G-code files.

## Getting Started

### Prerequisites

- Python 3
- Flask
- SQLite3

### Installation

1. Clone the repository:
git clone [repository-url]

2. Navigate to the project directory:

cd [project-name]

3. Install the required Python packages:

pip install -r requirements.txt

4. Run the Flask application:

python app.py

5. The application should now be running on `http://localhost:5000`.

## Usage

- **Uploading G-code Files:**
- Navigate to `http://localhost:5000` and use the file upload form to upload a G-code file.

- **Viewing Uploaded Files:**
- After uploading, view the list of uploaded files along with their metadata.

## Contributing

Contributions to the project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to all the contributors who have helped with the development of thi