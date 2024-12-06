from datetime import datetime
import os
import re

LOG_BASEPATH = './logs/'
LOG_FILE_SHIFT = True

def strip_and_extract(s: str) -> tuple[str|int]:
    match = re.search(r'(_\d+)$', s)
    if match:
        stripped_part = match.group(1)  # The matched part (e.g., "_1", "_99")
        return s[:match.start()], stripped_part
    return s, 0

def generate_next_log_fn(fn: str) -> str:
    ext_stripped, ext = fn[:fn.rfind('.')], fn[fn.rfind('.') + 1 :]
    num_stripped, num = strip_and_extract(ext_stripped)

    fn = num_stripped
    while os.path.exists(fn):
        num += 1
        fn = f'{num_stripped}_{num}.{ext}'
    return fn

def shift_logs(base_fn: str):
    ext_stripped, ext = base_fn[:base_fn.rfind('.')], base_fn[base_fn.rfind('.') + 1 :]
    
    for i in range(int(1e3), 0, -1):
        fn = f'{ext_stripped}_{i}.{ext}'
        nfn = f'{ext_stripped}_{i + 1}.{ext}'
        if os.path.exists(fn):
            os.rename(fn, nfn)
    
    fn = f'{ext_stripped}.{ext}'
    nfn = f'{ext_stripped}_1.{ext}'
    if os.path.exists(fn):
        os.rename(fn, nfn)

def generate_log_fn(shift=True) -> str:
    if not os.path.exists(LOG_BASEPATH):
        os.makedirs(LOG_BASEPATH)
    
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M")
    fn = f'log_{formatted_time}.txt'
    
    if shift:
        shift_logs(os.path.join(LOG_BASEPATH, fn))
    else:
        i = 1
        while os.path.exists(os.path.join(LOG_BASEPATH, fn)):
            fn = f'log_{formatted_time}_{i}.txt'
            i += 1
    
    return os.path.join(LOG_BASEPATH, fn)

class Logger:
    def __init__(self):
        self.log_list = []
        self.log_times = []
        self.log_colors = []
        self.log_timeits = []
        
        self.log_widget = None
        self.last_log_location = None
    
        #if not os.path.exists(LOG_BASEPATH):
            #os.makedirs(LOG_BASEPATH)
    
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
        self.log(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        
        if fn is None:
            if self.last_log_location is None:
                fn = generate_log_fn(shift=LOG_FILE_SHIFT)
            else:
                fn = generate_next_log_fn(self.last_log_location)
        
        with open(fn, 'w') as fout:
            fout.write(self.get_plain_text())
        self.last_log_location = fn


logger = Logger()
logger.log('Log started')