import Famcy

def main(args):
	content = """from Famcy import create_app

app = create_app('%s',True)

if __name__ == "__main__":
    app.run()"""% (args[0])

	f = open(Famcy.famcy_dir + "/wsgi.py", "w")
	f.write(content)
	f.close()

	print("Deployed to wsgi")