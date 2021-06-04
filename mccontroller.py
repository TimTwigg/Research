import keyboard as kb
import mouse
import time
import json
import re
import win32clipboard as w32

class MCController:
    """
    Controller functionality. Simulates keyboard and mouse events to programmatically play minecraft.
    
    NOTE: Uses win32keyboard to access system clipboard. Use on other operating systems not currently supported.
    NOTE: Currently has no input checking or error management.
    """
    # time required to move 1 block
    _block_time = 0.23
    # startup time allowed to focus the game after starting the program
    _wait_timer = 3
    # location of log file
    _log_file = "D:.minecraft\\logs\\latest.log"
    
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
        """
        Use system clipboard to paste command into minecraft.
        
        Ctrl-V operation requires more work, occasionally fails to paste command, creating an error message 
        in the log file which cascades into the program when the log file is read.
        """
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
        """
        Center the player on their current block.
        
        Center is defined as x.5 y z.5 ie: 100.5 64 -90.5
        """
        pos = [int(i) for i in self.get_player_pos()]
        self.command(f"tp @p {'-' if pos[0]<0 else ''}{abs(pos[0]) + 0.5} {pos[1]} {'-' if pos[2]<0 else ''}{abs(pos[2]) + 0.5}")
        
    def get_player_pos(self) -> [float]:
        """
        Use minecraft command to print player position to chat (and then to log file), then read log file and return position.
        """
        self.command("data get entity @p Pos")
        s = self.read_log_data()
        s = s[len(s) - s[::-1].find("["):-1]
        return [float(i[:-1]) for i in s.split(", ")]
    
    def get_player_data(self) -> dict:
        """
        Use minecraft command to print player data to chat (and then to log file), then read log file and analyze into json format.
        """
        self.command("data get entity @p")
        s = self.read_log_data()
        s = s[s.find("{"):]
        
        # add "" to keys
        keys = set(re.findall("[a-zA-Z]+(?=: )", s))
        for k in keys:
            pat = "(?<!\w)" + k
            s = re.sub(pat, f'"{k}"', s)
        
        # add "" to values
        values = re.findall("(?<=: )[\w.-]+(?=,|}|$)", s)
        for v in values:
            pat = "(?<=: )" + v + "(?=,|})"
            s = re.sub(pat, f'"{v}"', s)
        
        # fix UUID error
        ind = s.find("UUID") + 8
        s = s[:ind] + s[ind + 3:]
        
        # fix decimals/floats with 'd' or 'f' at end
        to_fix = set(re.findall("[\d.]+[df]", s))
        for i in to_fix:
            s = s.replace(i, i[:-1])
        
        return json.loads(s)
        
    def read_log_data(self) -> str:
        """
        Access minecraft log file and return last chat entry.
        """
        time.sleep(0.25)
        kb.press_and_release("escape")
        kb.press_and_release("escape")
        
        with open(self._log_file, "r") as f:
            lines = [l for l in f if "CHAT" in l]
        return lines[-1].strip()
