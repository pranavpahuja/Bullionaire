from nicegui import ui

def dashboard():
    @ui.page('/dashboard')
    def dashboard_page_def():
        with ui.row().classes('h-screen w-screen justify-center items-center gap-4'):
            ui.label('Welcome to Buillionaire').classes('text-2xl font-bold')
            ui.label('chart here')