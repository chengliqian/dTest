# Authour :chenglq
from django.utils.safestring import mark_safe

class Pager(object):
    def __init__(self,current_page):
        self.current_page = int(current_page)
    @property
    def start(self):
        return (self.current_page-1)*10

    @property
    def end(self):
        return self.current_page*10

    def page_str(self,all_item,base_url):
        all_page,div = divmod(all_item,10)
        if div>0:
            all_page+=1
        page_list = []
        if all_page<=5:
            start = 1
            end = all_page
        else:
            if self.current_page <=3:
                start = 1
                end = 5+1
            else:
                start = self.current_page-2
                end = self.current_page+3
                if self.current_page+3>all_page:
                    start = all_page-4
                    end = all_page+1
        for i in range(start,end):
            if i == self.current_page:
                temp = '<a style="color:lightblue;font-size:20px;padding:5px" href="%s?page=%d">%d</a>'%(base_url,i,i)
            else:
                temp = '<a style="padding:5px" href="%s?page=%d">%d</a>' % (base_url, i, i)
            page_list.append(temp)

        if self.current_page>1:
            pre_page = '<a href="%s?page=%d">上一页</a>'%(base_url,self.current_page-1)
        else:
            pre_page = '<a href="javascript:void(0);">上一页</a>'

        if self.current_page>=all_page:
            next_page = '<a href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a href ="%s?page=%d">下一页</a>'%(base_url,self.current_page+1)

        page_list.insert(0,pre_page)
        page_list.append(next_page)

        return  mark_safe("".join(page_list))