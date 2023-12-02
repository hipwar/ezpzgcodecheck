from flask import Flask, request, redirect, url_for, render_template
import os
import sqlite3
from datetime import datetime
from pygcode import Line, GCodeRapidMove, GCodeLinearMove
from pygcode.exceptions import GCodeWordStrError
import json

app = Flask(__name__)

def process_file(file_path):
    file_size = os.path.getsize(file_path)
    upload_time = datetime.now()
    conn = sqlite3.connect('./db/database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO uploads (filename, filepath, filesize, uploadtime) 
        VALUES (?, ?, ?, ?)
    ''', (os.path.basename(file_path), file_path, file_size, upload_time))
    conn.commit()
    conn.close()

@app.route('/parse-gcode/<filename>')
def parse_gcode(filename):
    file_path = os.path.join('uploads', filename)
    move_commands = []
    with open(file_path, 'r') as file:
        for line_text in file:
            try:
                line = Line(line_text)
                if line.gcodes:
                    gc = line.gcodes[0]
                    if isinstance(gc, (GCodeRapidMove, GCodeLinearMove)):
                        # Convert Word objects to float or use 0.0 as default
                        x = gc.params.get('X', 0.0) if 'X' in gc.params else 0.0
                        y = gc.params.get('Y', 0.0) if 'Y' in gc.params else 0.0
                        z = gc.params.get('Z', 0.0) if 'Z' in gc.params else 0.0
                        move_commands.append({"x": float(x), "y": float(y), "z": float(z)})
            except GCodeWordStrError as e:
                print(f"Error parsing line: {line_text.strip()} - {e}")


    output_path = os.path.join('static', 'parsed_gcode.json')
    with open(output_path, 'w') as out_file:
        json.dump(move_commands, out_file)

    return "G-code parsed. File saved at " + output_path

def get_latest_upload():
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM uploads ORDER BY uploadtime DESC LIMIT 1')
    latest_upload = cursor.fetchone()

    conn.close()
    return latest_upload

@app.route('/')
def index():
    return render_template('upload_form.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save('uploads/' + uploaded_file.filename)
        process_file(file_path)
        
        latest_upload = get_latest_upload()
        return render_template('upload.html', latest_upload=latest_upload)
    return redirect(url_for('index'))

@app.route('/visualize/<filename>')
def visualize_gcode(filename):
    # Path to the G-code file
    file_path = os.path.join('uploads', filename)

    # Process the G-code file for visualization
    # This might involve parsing the G-code and preparing data for visualization

    # For now, let's just pass the filename to a new template
    return render_template('visualize_gcode.html', filename=filename)

@app.route('/gallery')
def gallery():
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT filename, uploadtime FROM uploads')
    files = cursor.fetchall()

    conn.close()
    return render_template('gallery.html', files=files)

if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.47')
