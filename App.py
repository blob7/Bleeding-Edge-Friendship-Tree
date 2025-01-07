import os

if __name__ == "__main__":
    app_dir = r"\src\app\Homepage.py"
    current_dir = os.getcwd()
    os.system(f"streamlit run {current_dir}{app_dir}")