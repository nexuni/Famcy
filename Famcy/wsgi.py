from Famcy import create_app

app = create_app("MainFamcy", production=False)

if __name__ == "__main__":
    app.run()