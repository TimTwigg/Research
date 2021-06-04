import keyboard as kb
import mouse
import time, json, re, win32clipboard as w32

class MCController:
    _block_time = 0.23
    _wait_timer = 2
    
    def __init__(self):
        time.sleep(self._wait_timer)
        
    def __getattribute__(self, *args):
        if args[0] in ["forward", "left", "right", "back", "jump_up", "jump_down", "turn"]:
            time.sleep(0.25)
        return super().__getattribute__(*args)
    
    def presskey(self, key: str, n: int = 1):
        kb.press(key)
        time.sleep(self._block_time * n)
        kb.release(key)
        
    def repeatkey(self, key: str, repeat: int = 2):
        for _ in range(repeat):
            self.presskey(key)
            time.sleep(0.005)
            
    def forward(self, n: int = 1):
        self.presskey("w", n)
        
    def left(self, n: int = 1):
        self.presskey("a", n)
    
    def right(self, n: int = 1):
        self.presskey("d", n)
        
    def back(self, n: int = 1):
        self.presskey("s", n)
        
    def _turn(self, x, y):
        self.command(f"tp @p ~ ~ ~ {x} {y}")
        #self.center()
        
    def turn(self, direction):
        dirs = {
            "north": (180.0, "~"),
            "east": (-90.0, "~"),
            "west": (0.0, "~"),
            "south": (90, "~"),
            "straight": ("~", 0.0),
            "around": ("~180", "~"),
            "up": ("~", -90),
            "down": ("~", 90),
            "left": ("~-90", "~"),
            "right": ("~90", "~")}
        self._turn(*dirs[direction])
        
    def jump_up(self, n: int = 1):
        kb.press("w")
        kb.press("space")
        time.sleep(0.1)
        kb.release("space")
        time.sleep(0.18)
        kb.release("w")
        if n > 1:
            self.jump_up(n - 1)
            
    def jump_down(self, n: int = 1):
        self.command("tp @p ~ ~ ~ ~ 75")
        self.forward(n)
        self.command("tp @p ~ ~ ~ ~ 40")
            
    def click(self, button: str):
        mouse.click(button)
        time.sleep(0.25)
        
    def scroll(self, direction: str, repeat: int = 1):
        for _ in range(repeat):
            dirs = {
                "up": 1,
                "down": -1}
            mouse.wheel(dirs[direction])
            time.sleep(0.25)
    
    def command(self, cmd: str):
        w32.OpenClipboard()
        w32.EmptyClipboard()
        w32.SetClipboardText(cmd)
        w32.CloseClipboard()
        time.sleep(0.005)
        
        kb.press_and_release("/")
        
        kb.press("ctrl")
        time.sleep(0.05)
        kb.press("v")
        time.sleep(0.05)
        kb.release("v")
        kb.release("ctrl")
        
        kb.press_and_release("enter")
        
    def center(self):
        pos = [int(i) for i in self.get_player_pos()]
        self.command(f"tp @p {'-' if pos[0]<0 else ''}{abs(pos[0]) + 0.5} {pos[1]} {'-' if pos[2]<0 else ''}{abs(pos[2]) + 0.5}")
        
    def get_player_pos(self):
        self.command("data get entity @p Pos")
        s = self.read_log_data()
        s = s[len(s) - s[::-1].find("["):-1]
        return [float(i[:-1]) for i in s.split(", ")]
    
    def get_player_data(self):
        self.command("data get entity @p")
        s = self.read_log_data()
        s = s[s.find("{"):]
        
        keys = set(re.findall("[a-zA-Z]+(?=: )", s))
        for k in keys:
            pat = "(?<!\w)" + k
            s = re.sub(pat, f'"{k}"', s)
        
        values = re.findall("(?<=: )[\w.-]+(?=,|}|$)", s)
        for v in values:
            pat = "(?<=: )" + v + "(?=,|})"
            s = re.sub(pat, f'"{v}"', s)
        
        # fix UUID error
        ind = s.find("UUID") + 8
        s = s[:ind] + s[ind + 3:]
        
        # fix floats with 'd' at end
        to_fix = set(re.findall("[\d.]+[df]", s))
        for i in to_fix:
            s = s.replace(i, i[:-1])
        
        return json.loads(s)
        
    def read_log_data(self):
        time.sleep(0.25)
        kb.press_and_release("escape")
        kb.press_and_release("escape")
        
        with open("D:.minecraft\\logs\\latest.log", "r") as f:
            lines = [l for l in f if "CHAT" in l]
        return lines[-1].strip()
