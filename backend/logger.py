from datetime import datetime

class Logger:
    def __init__(self):
        self.log_list = []
        self.log_times = []
        self.log_colors = []
        self.log_timeits = []
        
        self.log_widget = None
        self.last_log_location = None
    
    def get_text(self):
        return self.log_list
    
    def get_plain_text(self):
        return '\n'.join(self.log_list) if len(self.log_list) > 0 else ''
    
    def register_widget(self, widget):
        self.log_widget = widget
        
        if len(self.log_list) > 0:
            for line, color, log_time, timeit in zip(self.log_list, self.log_colors, self.log_times, self.log_timeits):
                if timeit:
                    line = f'[{log_time.strftime("%H:%M:%S.%f")[:-4]}] ' + line
                self.log_widget.add_line(line, color=color)
    
    def log(self, line, color=None, timeit=True):
        if color is None:
            color = 'black'
        if not color.startswith('#'):
            if color == 'black':
                color = '#000000'
            elif color == 'grey':
                color = '#555555'
            elif color == 'red':
                color = '#ff2222'
            elif color == 'green':
                color = '#22ff22'
            elif color == 'blue':
                color = '#2222ff'
            else:
                color = '#000000'
        
        self.log_list.append(line)
        self.log_colors.append(color)
        self.log_times.append(datetime.now())
        self.log_timeits.append(timeit)
        if timeit:
            line = f'[{datetime.now().strftime("%H:%M:%S.%f")[:-4]}] ' + line
        
        if self.log_widget is not None:
            self.log_widget.add_line(line, color=color)
    
    def save(self, fn=None):
        if fn is None:
            if self.last_log_location is None:
                self.log("Error: no designated location to write log")
                return
            fn = self.last_log_location
        self.last_log_location = fn
        with open(fn, 'w') as fout:
            fout.write(self.get_plain_text())


logger = Logger()
logger.log('Log started')