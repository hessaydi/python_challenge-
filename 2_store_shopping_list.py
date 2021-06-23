# You heve to install flask, flask_marshmallow, flask_restful, flask_cors 
# and flask_sqlalchemy modulesin you envirnment before you precceed 
# the execution of this script
# Importent: Go to the line 180

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy support PostgreSQL databases
from flask_marshmallow import Marshmallow
# from flask_restful import Api, Resource
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Development database change it to refer into your own database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
CORS(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopping_id = db.Column(db.Integer, db.ForeignKey('shopping.id'),
        nullable=False)
    title = db.Column(db.String(50))

    def __repr__(self):
        return f'<Article {self.title}>'

class Shopping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    articles = db.relationship('Article', backref='shopping', lazy=True)

    def __repr__(self):
        return f'<Shopping {self.title}>'


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ("id", "title")

class ShoppingSchema(ma.Schema):
    class Meta:
        fields = ("id", "title")

shopping_schema = ShoppingSchema()
shoppings_schema = ShoppingSchema(many=True)
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


class ArticleListResource(Resource):
    def get(self):
        articles = Article.query.all()
        return articles_schema.dump(articles), 200

    def post(self):
        new_article = Article(
            title=request.json['title'],
            shopping_id=request.json['shopping_id']
        )
        db.session.add(new_article)
        db.session.commit()
        return article_schema.dump(new_article), 201
    def delete(self):
        try:
            num_rows_deleted = db.session.query(Article).delete()
            db.session.commit()
        except:
            db.session.rollback()
        return f'{num_rows_deleted}', 204
class ArticleSearchResource(Resource):
    def get(self, search):
        articles = Article.query.filter(Article.title.like('%' + search + '%'))
        return articles_schema.dump(articles), 201


class ArticleResource(Resource):
    def get(self, article_id):
        article = Article.query.get_or_404(article_id)
        return article_schema.dump(article), 200

    def put(self, article_id):
        article = Article.query.get_or_404(article_id)
        if 'title' in request.json:
            article.title = request.json['title']
        if 'shopping_id' in request.json:
            article.shopping_id = request.json['shopping_id']

        db.session.commit()
        return article_schema.dump(article), 200

    def patch(self, article_id):
        article = Article.query.get_or_404(article_id)

        if 'title' in request.json:
            article.title = request.json['title']
        if 'shopping_id' in request.json:
            article.shopping_id = request.json['shopping_id']

        db.session.commit()
        return article_schema.dump(article)

    def delete(self, article_id):
        article = Article.query.get_or_404(article_id)
        db.session.delete(article)
        db.session.commit()
        return 'f{article_id}', 204


class ShoppingListResource(Resource):
    def get(self):
        shoppings= Shopping.query.all()
        return shoppings_schema.dump(shoppings), 200

    def post(self):
        new_shopping = Shopping(
            title=request.json['title'],
        )
        db.session.add(new_shopping)
        db.session.commit()
        return shopping_schema.dump(new_shopping), 201

    def delete(self):
        try:
            num_rows_deleted = db.session.query(Shopping).delete()
            db.session.commit()
        except:
            db.session.rollback()
        return f'{num_rows_deleted}', 204

class ShoppingSearchResource(Resource):
    def get(self, search):
        shoppings = Shopping.query.filter(Shopping.title.like('%' + search + '%'))
        return shoppings_schema.dump(shoppings), 201


class ShoppingResource(Resource):
    def get(self, shopping_id):
        shopping = Shopping.query.get_or_404(shopping)
        return Shopping_schema.dump(Shopping), 200

    def put(self, shopping_id):
        shopping = Shopping.query.get_or_404(shopping_id)
        if 'title' in request.json:
            Shopping.title = request.json['title']

        db.session.commit()
        return Shopping_schema.dump(shopping), 200

    def patch(self, shopping_id):
        shopping = Shopping.query.get_or_404(shopping_id)

        if 'title' in request.json:
            Shopping.title = request.json['title']
            
        db.session.commit()
        return Shopping_schema.dump(shopping)

    def delete(self, shopping_id):
        shopping = Shopping.query.get_or_404(shopping_id)
        db.session.delete(shopping)
        db.session.commit()
        return 'f{shopping_id}', 204

api.add_resource(ArticleListResource, '/articles')
api.add_resource(ArticleSearchResource, '/articles/search/<search>')
api.add_resource(ArticleResource, '/article/<int:article_id>')


api.add_resource(ShoppingListResource, '/shoppings')
api.add_resource(ShoppingSearchResource, '/shoppings/search/<search>')
api.add_resource(ShoppingResource, '/shopping/<int:article_id>')


if __name__ == '__main__':
    db.create_all()  #uncomment this line if you run this for the first time
    app.run(debug=True)
