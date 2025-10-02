from nicegui import ui
import json

# Load users from JSON
with open('users.json') as f:
    users_data = json.load(f)['users']


def check_credentials(username, password):
    return any(u['username'] == username and u['password'] == password for u in users_data)


def register_login():
    @ui.page('/login')
    def login_page():
        # Full-screen column centered both vertically and horizontally
        with ui.column().classes('h-screen w-screen justify-center items-center gap-4'):
            ui.label('🔐 Login').classes('text-3xl font-bold')

            username_input = ui.input('Username').props('autofocus')
            password_input = ui.input('Password', password=True)

            message = ui.label('').classes('text-red-500')

            def login_action():
                username = username_input.value
                password = password_input.value
                if check_credentials(username, password):
                    ui.notify(f'Welcome {username}!', type='positive')
                    ui.navigate.to('/home')  # Redirect to home
                else:
                    message.text = '❌ Invalid username or password'

            ui.button('Login', on_click=login_action).classes('w-32')