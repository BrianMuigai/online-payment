from app import create_app, db, cli
from app.models import Transaction

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'Transaction': Transaction}

if __name__ == '__main__':
	app.run(debug=True, port=8080)