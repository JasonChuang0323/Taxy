import sys
print(sys.path)
from app import create_app


app = create_app()

if __name__ == '__main__':
    print("hello")
    app.run(debug=True)