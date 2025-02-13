from flask import Flask, render_template
import pygments
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import os
import subprocess

def gitIsInstalled() -> bool:
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def cloneRepo(repoUrl: str = "https://github.com/DHMorse/luigisHomework") -> None:
    if not os.path.exists("luigisHomework"):
        try:
            subprocess.run(["git", "clone", repoUrl], check=True)
            print(f"Successfully cloned {repoUrl}")
        
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone repository: {e}")
        
        except Exception as e:
            print(f"An error occurred: {e}")
        return
    else:
        gitPull()

def gitPull() -> None:
    try:
        subprocess.run("cd luigisHomework && git pull", shell=True, check=True)
        print("Successfully pulled changes")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull changes: {e}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def main() -> None:
    if not gitIsInstalled():
        print("Git is not installed")
        return
    
    cloneRepo()

    app = Flask(__name__)
    
    @app.route('/')
    def index():
        # Sample Python code - you can replace this with any Python file content
        with open('/home/daniel/Documents/myCode/luigisHomeworkWebViewer/luigisHomework/myCode/age.py', 'r') as file:
            code = file.read()
        
        # Generate highlighted HTML
        highlighted_code = highlight(code, PythonLexer(), HtmlFormatter())
        
        # Get the CSS styles
        css_styles = HtmlFormatter(style='solarized-dark').get_style_defs('.highlight')

        print(css_styles)

        return render_template('index.html', 
                            code=highlighted_code, 
                            css_styles=css_styles)


    app.run(debug=True)

if __name__ == "__main__":
    main()