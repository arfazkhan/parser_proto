from flask import Flask, request, render_template
from pdf_parser import PdfParser
import sys
from contextlib import redirect_stdout

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle the file upload from the web form
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            file_name = uploaded_file.filename  # Get the file name
            file_path = "uploads/" + file_name
            uploaded_file.save(file_path)
            pdf_parser = PdfParser(file_path)  # Initialize PdfParser with the file path

            # Capture the printed output
            with redirect_stdout(sys.stdout):
                result = pdf_parser.parse_pdf(file_name, debug_val=True)

            return render_template("results.html", result=result)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
