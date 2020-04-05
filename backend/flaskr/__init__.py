import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy.sql.expression import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    
    all_questions = [question.format() for question in questions]
    questions_in_page = all_questions[start:end]
    
    return questions_in_page

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
  
    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
        return response

    '''
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        array = []
        for category in categories:
            array.append(category.type)
        
        if len(categories) == 0:
            abort(404)
        
        return jsonify({
            'success': True,
            'categories': array,
            'total_categories': len(Category.query.all())
        })


    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''
    @app.route('/questions')
    def get_questions():
        try:
            current_category_id = request.args.get('category', 1, type=int) # defaults to category id 1 if not provided
            current_category = Category.query.filter(Category.id == current_category_id).one_or_none()
            
            if current_category is None:
                abort(404)
                
            questions = Question.query.order_by(Question.id).filter(Question.category == current_category_id).all()
            questions_in_page = paginate_questions(request, questions)

            categories = Category.query.order_by(Category.id).all()
            array = []
            for category in categories:
                array.append(category.type)

            if len(categories) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'questions': questions_in_page,
                'total_questions': len(Question.query.all()),
                'current_category': current_category.type,
                'categories': array
            })
        
        except:
            abort(422)

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True
            })
        
        except:
            abort(400)

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''
    @app.route('/questions', methods=['POST'])
    def create_questions():
        
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
            
        try:
            # Check if question is passed through. If TRUE, request is for creating new a question
            if question:
                question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                question.insert()
                
                return jsonify({
                    'success': True,
                    'id': question.id
                })
            # Else means request is for searching questions
            else:
                current_category_id = body.get('category_id', None)
                    
                questions = Question.query.order_by(Question.id)
        
                return_current_category = []
            
                if current_category_id:
                    current_category = Category.query.filter(Category.id == current_category_id).one_or_none()
                        
                    if current_category is None:
                        abort(404)
                        
                    questions = questions.filter(Question.category == current_category_id)
                    
                    return_current_category = current_category.type
                
                if search_term:
                    questions = questions.filter(Question.question.ilike('%{}%'.format(search_term)))
                        
                questions = questions.all()
                questions_in_page = paginate_questions(request, questions)
                
                return jsonify({
                        'success': True,
                        'questions': questions_in_page,
                        'total_questions': len(Question.query.all()),
                        'current_category': return_current_category
                })

            
        except:
            abort(422)
            

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 

    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''
    
    @app.route('/categories/<int:cat_id>/questions')
    def get_questions_by_category(cat_id):
        current_category_id = cat_id + 1
        
        try:
            current_category = Category.query.filter(Category.id == current_category_id).one_or_none()
            
            if current_category is None:
                abort(404)
                
            questions = Question.query.order_by(Question.id).filter(Question.category == current_category_id).all()
            questions_in_page = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': questions_in_page,
                'total_questions': len(Question.query.all()),
                'current_category': current_category.type
            })
        
        except:
            abort(422)


    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', [])
            quiz_category_id = body.get('quiz_category', None)
            if quiz_category_id:
                quiz_category_id = quiz_category_id.get('id', None)
            
            if quiz_category_id:
                quiz_category_id = int(quiz_category_id) + 1
                current_question = Question.query.order_by(func.random()).filter(Question.category == quiz_category_id)
                for a in previous_questions:
                    current_question = current_question.filter(Question.id != a)
                current_question = current_question.first()
            else:
                current_question = Question.query.order_by(func.random()).first()
                
            if current_question:
                return jsonify({
                    'success': True,
                    'question': {
                        'id': current_question.id,
                        'question': current_question.question,
                        'answer': current_question.answer,
                        'category': current_question.category,
                        'difficulty': current_question.difficulty
                    }
                })
            else:
                return jsonify({
                    'success': True
                })
                

        
        except:
            abort(422)
    
    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
        }), 404
                              
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
        }), 422
  
    return app

    