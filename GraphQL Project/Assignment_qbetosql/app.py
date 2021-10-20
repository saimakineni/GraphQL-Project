#Python HTTP server for GraphQL.
from flask import Flask
from flask_graphql import GraphQLView
from qbe_tester import schema
from flask_cors import CORS
from flask import render_template


app = Flask(__name__)
CORS(app)

app.add_url_rule('/', view_func=GraphQLView.as_view('graphql',
                 schema=schema, graphiql=True))
app.run(debug=True)