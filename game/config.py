class Config:
    """Singleton pattern for game configuration"""
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__instance._init_config()

        return cls.__instance
    
    def _init_config(self):
        self.width = 800
        self.height = 600

        self.n_cells_x = 40
        self.n_cells_y = 30

        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'gray': (128, 128, 128),
            'green': (0, 255, 0)
        }

        self.tick_interval = 200

        self.ui_padding = 20
        self.button_width = 100
        self.button_height = 30
