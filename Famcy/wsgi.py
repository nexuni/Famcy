from Famcy import create_app

app = create_app("FamcyTest", False)

if __name__ == "__main__":
    app.run()