import datetime as dt
from db import db_connect
class MemoManager:
    def __init__(self):
        self.status = {
            "keyword": None,
            "important": False,
            "sort_by": "all",
            "sort_order": None
        }
    def add_memo(self, content, important=False , user_id = "guest"): # 메모 추가
        content = content.strip()
        if not content:
            return
        date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = db_connect()
        cursor = conn.cursor()
        sql = "INSERT INTO memos (user_id, content, important, deleted, created_at) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, content, important, False, date))
        conn.commit()
        conn.close()
    def view_memos(self): # 메모 보기
        conn = db_connect()
        cursor = conn.cursor()
        sql = "SELECT id,content, important, deleted, created_at FROM memos"
        cursor.execute(sql)
        memos = cursor.fetchall()
        conn.close()
        if not memos:
            return []
        view_memos = []
        for memo in memos:
            memo = memo.copy()
            if memo["deleted"]:
                continue
            view_memos.append(memo)
        return view_memos
    def delete_memo(self, id): # 메모 삭제
        try:
            id = int(id)
        except:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "UPDATE memos SET deleted = %s WHERE id = %s"
        cursor.execute(sql, (True, id))
        conn.commit()
        conn.close()
        return
    def set_important(self, id): # 중요 표시/해제
        try:
            id = int(id)
        except:
            return
        conn = db_connect()
        cursor = conn.cursor()
        sql = "UPDATE memos SET important = NOT important WHERE id = %s"
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
        return
    def set_keyword(self, keyword): # 검색어 설정
        keyword = keyword.strip()
        if not keyword:
            self.status["keyword"] = None
        else:
            self.status["keyword"] = keyword
        return
    def set_sort_by(self, sort_by): # 정렬 기준 설정
        if sort_by != self.status["sort_by"]:
            self.status["sort_by"] = sort_by
            self.status["sort_order"] = "asc"
        elif self.status["sort_order"] == "asc":
            self.status["sort_order"] = "desc"
        else:
            self.status["sort_by"] = "all"
            self.status["sort_order"] = None
        return
    def set_status_important(self): # 중요보기 설정
        self.status["important"] = not self.status["important"]
        return
    def get_filtered_memos(self,memos): # 필터링된 메모 가져오기
        filtered_memos = memos
        if not filtered_memos:
            return []
        keyword = self.status["keyword"]
        if keyword is not None:
            filtered_memos  = [memo for memo in filtered_memos if keyword in memo["content"]]
        return filtered_memos
    def get_sorted_memos(self,memos): # 정렬된 메모 가져오기
        sorted_memos = memos
        if not sorted_memos:
            return []
        sort_by = self.status["sort_by"]
        sort_order = self.status["sort_order"]
        if self.status["sort_by"] != "all":
            sorted_memos = sorted(sorted_memos, key=lambda x: x[sort_by], reverse=(sort_order == "desc"))
        return sorted_memos
    def get_important_memos(self,memos): # 중요 표시된 메모 가져오기
        important_memos = memos
        if not important_memos:
            return []
        if self.status["important"]:
            important_memos = [memo for memo in important_memos if memo["important"]]
        return important_memos
    def get_final_memos(self): # 최종적으로 보여줄 메모 가져오기
        memos = self.view_memos()
        memos = self.get_filtered_memos(memos)
        memos = self.get_important_memos(memos)
        memos = self.get_sorted_memos(memos)
        return memos
    def reset_status(self): # 상태 초기화
        self.status = {
            "keyword": None,
            "important": False,
            "sort_by": "all",
            "sort_order": None
        }
        return
    