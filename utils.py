class UI:
    status = {
        "s": "STATUS",
        "m": "MESSAGE",
        "e": "ERROR"
    }
    
    def show(self, type, msg):
        print(f"[{self.status[type]}] {msg}")