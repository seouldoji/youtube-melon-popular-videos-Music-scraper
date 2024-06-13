from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/download')
def download_file():
    file_path = 'kinokuniya_bestsellers.csv'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found!", 404

if __name__ == '__main__':
    app.run(debug=True)
