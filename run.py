from src import create_app
import config

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
else:
    app = create_app()
    