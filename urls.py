import webapp2

app = webapp2.WSGIApplication([
								# pages
                                ('/', 'views.pages.MainPage'),
                                ('/add_bookmark', 'views.pages.AddBookmark')
    ])