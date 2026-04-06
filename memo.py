import datetime as dt
class MemoManager:
    def __init__(self):
        self.memos = []
        self.status = {
            "keyword": "",
            "important": False,
            "sort_by": "all",
            "sort_order": None
        }
    def add_memo(self, content, important=False):
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memo = {
            "content": content,
            "important": important,
            "deleted": False,
            "date": date
        }
        self.memos.append(memo)
    def view_memos(self):
        if not self.memos:
            return
        view_memos = []
        for idx,memo in enumerate(self.memos):
            memo = memo.copy()
            memo["index"] = idx
            if memo["deleted"]:
                continue
            self.view_memos.append(memo)
        return view_memos
    def delete_memo(self, index):
        try:
            original_index = int(index)
        except:
            return
        self.memos[original_index]["deleted"] = True
        return
    def set_important(self, index):
        try:
            original_index = int(index)
        except:
            return
        self.memos[original_index]["important"] = True
        return
    def set_keyword(self, keyword):
        keyword = keyword.strip()
        if not keyword:
            return 
        self.status["keyword"] = keyword
        return


        

        