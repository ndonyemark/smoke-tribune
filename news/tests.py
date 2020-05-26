from django.test import TestCase
from .models import Editor, Article, Tags
import datetime as dt

# Create your tests here.

class EditorTestClass(TestCase):

    def setUp(self):
        self.mark = Editor(first_name='Mark', last_name='Ndonye', email='ndonyemark@gmail.com')

    # Testing an instance

    def test_instance(self):
        self.assertTrue(isinstance(self.mark, Editor))
    
    def test_save_method(self):
        self.mark.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors)>0)

class ArticleTestClass(TestCase):
    def setUp(self):
        self.mark = Editor(first_name='Mark', last_name='Ndonye', email='ndonyemark@gmail.com')
        self.mark.save_editor()

        # create new tag and save it

        self.new_tag = Tags(name = 'testing')
        self.new_tag.save()

        self.new_article = Article(title='Test Article', post = 'This is a random test Post', editor = self.mark)

        self.new_article.save()

        self.new_article.tags.add(self.new_tag)

    def tearDown(self):
        Editor.objects.all().delete()
        Tags.objects.all().delete()
        Article.objects.all().delete()
        
    def test_get_news_today(self):
        todays_news=Article.todays_news()
        self.assertTrue(len(todays_news) > 0)
    
    def test_get_news_by_date(self):
        test_date = '2017-03-17'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) == 0)
