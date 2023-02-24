import curses

from threading import Lock
import time
class ScreenHandler:
  def __init__(self, config, wrapper):
    self.config = config
    self.wrapper = wrapper

    self.stdscr = None
    self.input_window = None
    self.output_window = None
    self.screen_h = 0
    self.screen_w = 0
    
    self.output_scroll_pos = 0
    self.prompt_string = " spsm >>"
    
    self.current_input = []
    
    self.error_handler = None
    self.input_handler = None
    
    self.screen_lock = Lock()
  
  def connect_error_handling(self, error_handler):
    self.error_handler = error_handler
    
  def connect_input_handler(self, input_handler):
    self.input_handler = input_handler

  def init_windows(self):
    
    # Initialize the curses screen
    self.stdscr = curses.initscr()

    # Enable keypad keys to be recognized
    self.stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()
    
    
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

    # Get the dimensions of the terminal window
    self.screen_h, self.screen_w = self.stdscr.getmaxyx()

    # Create the output window
    self.output_window = curses.newpad(self.screen_h*150, self.screen_w)
    self.output_window.move(self.screen_h - 4, 0)
    self.output_window.scrollok(True)

    # Create the input window
    self.input_window = curses.newwin(3, self.screen_w, self.screen_h - 3, 0)
    self.input_window.nodelay(True)
    self.input_window.keypad(True)
    self.refresh()

  def append_output(self, output, color=0):
    self.output_window.addstr(output, curses.color_pair(color))
    self.scroll_down()
    self.refresh()

  def scroll_down(self):
    self.output_scroll_pos += 1
    if self.output_scroll_pos > self._max_scroll_value():
      self.output_scroll_pos = self._max_scroll_value()
    
  def scroll_up(self):
    self.output_scroll_pos -= 1
    if self.output_scroll_pos < 0:
      self.output_scroll_pos = 0
      
  def format_screen(self):
    self.screen_h, self.screen_w = self.stdscr.getmaxyx()
    
    self.input_window.resize(3, self.screen_w)
    self.input_window.mvwin(self.screen_h - 4, 0)
    
    self.output_window.resize(self.screen_h*150, self.screen_w)
    
    self.refresh()

  def refresh_output_window(self):
    self.output_window.refresh(self.output_scroll_pos,0, 0,0, self.screen_h - 4, self.screen_w)

  def reset_input_window(self):
    self.refresh()

  def refresh(self):
    self.screen_lock.acquire()
    retry = False
    try:
      self.input_window.clear()
      self.input_window.border()
      self.input_window.addstr(1,1, self.prompt_string)
      self.input_window.addstr("".join(self.current_input))
      
      self.input_window.refresh()
      self.refresh_output_window()
    except curses.error:
      retry = True
    finally:
      self.screen_lock.release()
      if retry:
        time.sleep(0.1)
        self.refresh()

  def clear_input_window(self):
    self.input_window.clear()
    self.input_window.refresh()

  def cleanup(self):
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    
  def _max_scroll_value(self):
    return self.output_window.getyx()[0]
    
  #---- Input Decoding ----#
  def track_input(self):
    while self.wrapper.active:
      try:
        c = self.input_window.get_wch()
      except curses.error:
        continue
      
      if c == -1 or c == curses.ERR:
        continue
      elif c == curses.KEY_BACKSPACE or c == '^?' or c == '\b':
        if len(self.current_input) == 0:
          continue
        self.input_window.addstr("\b \b")
        self.current_input = self.current_input[:-1]
      elif c == curses.KEY_ENTER or c == '\n' or c == '\r':
        if len(self.current_input) == 0:
          continue
        command = ''.join(self.current_input)
        self.input_handler.handle_command(command)
        self.reset_input_window()
        self.current_input = []
      elif c == curses.KEY_RESIZE:
        try:
          self.format_screen()
        except curses.error:
          pass
      elif c == curses.KEY_UP:
        self.scroll_up()
        self.refresh_output_window()
      elif c == curses.KEY_DOWN:
        self.scroll_down()
        self.refresh_output_window()
      else:
        self.screen_lock.acquire()
        
        self.current_input.append(c)
        self.input_window.addch(c)
        
        self.screen_lock.release()
      self.input_window.refresh()