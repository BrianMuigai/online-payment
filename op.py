from app import create_app, db, cli
from app.models import Admin, DirectTransactions, EscrowTransactions

app = create_app()
cli.register(app)

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'Admin': Admin, 'DirectTransactions': DirectTransactions, \
	'EscrowTransactions':EscrowTransactions}

if __name__ == '__main__':
	app.run(debug=True, port=8080)