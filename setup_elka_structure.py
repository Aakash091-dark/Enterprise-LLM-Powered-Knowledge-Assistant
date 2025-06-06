import os

project_structure = {
    "elka": {
        "backend": [
            "app.py",
            "rag_engine.py",
            "model.py",
            "utils.py",
            "config.py"
        ],
        "frontend": [
            "app.py"
        ],
        "data": {
            "company_docs": [],
            "vector_store": []
        },
        "models": [
            "config.yaml"
        ],
        ".env": "",
        "Dockerfile": "",
        "requirements.txt": "",
        "README.md": ""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for file in content:
                file_path = os.path.join(path, file)
                open(file_path, 'a').close()
        else:
            # Single file
            file_path = os.path.join(base_path, name)
            open(file_path, 'a').close()

def main():
    print("Creating ELKA project structure...")
    create_structure(".", project_structure)
    print("✅ Structure created! Navigate into the 'elka' folder to start building.")

if __name__ == "__main__":
    main()
