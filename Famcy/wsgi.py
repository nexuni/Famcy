from Famcy import create_app

app = create_app('pms',True)

if __name__ == "__main__":
    app.run()