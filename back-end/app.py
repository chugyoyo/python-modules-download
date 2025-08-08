from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess
import os
import tempfile
import shutil
import zipfile

app = Flask(__name__)
CORS(app)  # 为整个应用开启跨域支持

@app.route('/endpoint', methods=['POST'])
def receive_data():
    # Check if the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    # Get the JSON data from the request
    data = request.get_json()

    # Extract the package name, Python version, and platform
    package_name = data.get('packageName')
    python_version = data.get('pythonVersion')
    platform = data.get('platform')

    if not package_name or not python_version or not platform:
        return jsonify({"error": "Package name, Python version, and platform are required"}), 400

    # Create a temporary directory to store the downloaded package
    temp_dir = tempfile.mkdtemp()

    try:
        # Download the package using pip
        download_command = (
            f"pip3 download --only-binary=:all: "
            f"--platform {platform} "
            f"--python-version {python_version} "
            f"--dest {temp_dir} {package_name}"
        )
        subprocess.run(download_command, shell=True, check=True)

        # Compress the entire temp_dir to a zip file
        zip_file_path = os.path.join(tempfile.gettempdir(), f"{package_name}.zip")
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add file to zip with relative path
                    zipf.write(file_path, os.path.relpath(file_path, temp_dir))

        # Send the compressed package file to the client
        return send_file(zip_file_path, as_attachment=True, download_name=f"{package_name}.zip")

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Failed to download package: {e}"}), 500

    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
        # Remove the zip file if it exists
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)

if __name__ == '__main__':
    app.run(debug=True)