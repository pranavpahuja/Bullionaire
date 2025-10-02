from backend.login import register_login
from components.elements import header
from nicegui import ui
from pages.landing import landing_page
from pages.aboutus import register_about
from pages.dashboard import dashboard
from pages.home import home_page

# Register all pages
register_login()
landing_page()
register_about()
dashboard()
home_page()

ui.run()
