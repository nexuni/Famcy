"""
This is the page definition file for Famcy. 
There are two variables very important, which
defines the page content: PAGE_HEADER and PAGE_CONTENT. 

PAGE_HEADER:
  * title: a list of titles of the sections on the page. It is usually put
    at the top of the section as a header. 
  * size: a list. defines section size. Options include half_inner_section
    and inner_section -> half means share two sections on one page
  * type: list of fblock type of the sections on the page. This should match the
    defined fblock name. 

PAGE_CONTENT:
  * a list of dictionary that defines the fblock sections on the page.  

example:
  PAGE_HEADER = {
  "title": ["Nexuni 員工後台"],
    "size": ["inner_section"],
    "type": ["display"]
}

PAGE_CONTENT = [
  {
      "values": [{
          "type": "displayParagraph",
          "title": "",
          "content": '''
**Nexuni 会社ウェブサイトの案内** 

  1. 希望能讓來到Nexuni的新朋友都能夠快速地學習並瞭解我們工作時會使用到的軟體、程式語言、工具等等。
  2. 作為能力考核的依據
  3. 整合所有公司內部的管理工具，如發票上傳、PO申請、報帳工具、打卡記錄等

快速入門:

  * 點擊總覽 -> 訓練網介紹（可以看到本網頁的所有的內容簡介
  * 點擊相關訓練內容 -> 開始練習
  * 點擊總覽 -> 學習進度裡面的進度報告（可以看到練習的成果）

（網頁內容的版權皆為Nexuni Co. 擁有）
''',
      },{
          "type": "displayTag",
          "title": "測試不知道這是用來幹嘛的Layout",
          "content": "到底Display Tag有什麼不一樣？",
      },
      {
          "type": "displayImage",
          "title": "下面這個解析度也太糟糕了吧",
          "img_name": "test.jpg", # This is gathered from static folder or _images_ user folder
      }]
    }
]
"""
import Famcy

PAGE_HEADER = {
    "title": ["折線圖模板", "柱狀圖模板", "更新折線圖模板"],
    "size": ["onefourth_inner_section", "threefourth_inner_section", "inner_section"],
    "type": ["line_chart", "bar_chart", "line_chart"],
}

line_chart_content_1 = Famcy.line_chart.generate_template_content()
line_chart_content_1.update({
		"title": "折線圖1"
	})

line_chart_content_2 = Famcy.line_chart.generate_template_content()
line_chart_content_2.update({
		"title": "折線圖2"
	})

bar_chart_content = Famcy.bar_chart.generate_template_content()
bar_chart_content.update({
		"title": "柱狀圖"
	})

PAGE_CONTENT = [line_chart_content_1, bar_chart_content, line_chart_content_2]

PAGE_CONTENT_OBJECT = Famcy.generate_content_obj(PAGE_HEADER, PAGE_CONTENT)