import os
from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG", False),
        host="0.0.0.0",
        port=os.environ.get("PORT", 5000)
    )
