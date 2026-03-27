import tornado.ioloop
import tornado.web
import os
import csv
import json
from datetime import datetime

class MainHandler(tornado.web.RequestHandler):
    def get(self, path=None):
        if not path:
            path = "index.html"
        if not os.path.exists(path):
            self.set_status(404)
            self.write("File not found")
            return
        self.render_file(path)

    def render_file(self, path):
        content_type = "text/html"
        if path.endswith(".css"): content_type = "text/css"
        elif path.endswith(".js"): content_type = "application/javascript"
        elif path.endswith(".png"): content_type = "image/png"
        elif path.endswith(".jpg") or path.endswith(".jpeg"): content_type = "image/jpeg"
        
        self.set_header("Content-Type", content_type)
        with open(path, 'rb') as f:
            self.write(f.read())

class ApplicationHandler(tornado.web.RequestHandler):
    def post(self):
        # We receive data as JSON or Multipart
        content_type = self.request.headers.get("Content-Type", "")
        
        data = {}
        file_name = ""
        
        if "multipart/form-data" in content_type:
            # Handle multipart form data
            for name, field_list in self.request.arguments.items():
                data[name] = field_list[0].decode('utf-8')
            
            if "fileUpload" in self.request.files:
                file_info = self.request.files["fileUpload"][0]
                file_name = file_info["filename"]
                # Save the file to an 'uploads' directory
                if not os.path.exists("uploads"):
                    os.makedirs("uploads")
                with open(os.path.join("uploads", file_name), 'wb') as f:
                    f.write(file_info["body"])
        else:
            # Handle JSON data
            data = json.loads(self.request.body.decode('utf-8'))
            file_name = data.get("fileUpload", "")

        # Save to CSV
        csv_file = 'applications.csv'
        file_exists = os.path.isfile(csv_file)
        
        fieldnames = [
            'fullName', 'dob', 'email', 'phone', 
            'institution', 'gpa', 'degree', 
            'language', 'testScore', 'faculty', 
            'program', 'motivation', 'fileUpload', 'timestamp'
        ]
        
        row_data = {k: data.get(k, "") for k in fieldnames}
        row_data['timestamp'] = datetime.now().isoformat()
        row_data['fileUpload'] = file_name
        
        try:
            with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(row_data)
            
            self.write({"status": "success"})
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            self.set_status(500)
            self.write({"status": "error", "message": str(e)})

def make_app():
    return tornado.web.Application([
        (r"/submit_application", ApplicationHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": ".", "default_filename": "index.html"}),
    ])

if __name__ == "__main__":
    app = make_app()
    port = 8001
    app.listen(port)
    print(f"Server started at http://localhost:{port}/application.html")
    tornado.ioloop.IOLoop.current().start()
