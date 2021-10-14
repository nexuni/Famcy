import json
import Famcy

class table(Famcy.FamcyBlock):
    """
    Represents the block to display
    table. 
    """
    def __init__(self, **kwargs):
        super(table, self).__init__(**kwargs)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "main_button_name": ["送出資料1", "送出資料2"],
            
            "input_button": "checkbox",                     # ("checkbox" / "radio" / "none")
            "input_value_col_field": "col_title1",          # if input_button != "none"

            "page_detail": True,                            # (true / false)
            "page_detail_content": "key_value",             # if page_detail == true: (key_value / HTML_STR => ["<p>line1</p>", "<p>line2</p>"])

            "toolbar": True,                                # (true / false)
            "page_footer": True,                            # (true / false)
            "page_footer_detail": {                         # if page_footer == true
                "page_size": 1,
                "page_list": [1, 2, "all"]
            },
            "submit_type": "update_block_html",
            "loader": False,
            "column": [[{
                    "title": 'col_title1 name',
                    "field": 'col_title1',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": 'col_title1 name',
                    "field": 'col_title1',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                },
                {
                    "title": 'col_title1 name',
                    "field": 'col_title1',
                    "rowspan": 1,
                    "align": 'center',
                    "valign": 'middle',
                    "sortable": True
                }
            ]],
            "data": [
                {
                    "col_title1": "row_content11",
                    "col_title2": "row_content12",
                    "col_title3": "row_content13"
                },
                {
                    "col_title1": "row_content21",
                    "col_title2": "row_content22",
                    "col_title3": "row_content23"
                },
                {
                    "col_title1": "row_content31",
                    "col_title2": "row_content32",
                    "col_title3": "row_content33"
                }
            ],
            "js_after_func_dict": {},
            "js_after_func_name": "empty_func",             # extra script which add after fblock item
            "header_script": "",            # extra script which add in header section
            "before_function": [],          # python function that you want to run before page refresh
        }

    def render_html(self, context, **configs):

        for action in context["before_function"]:
            action(context, **configs)

        main_button_html = ""
        index = 0
        for main_button_str in context["main_button_name"]:
            main_button_html += '<input id="mb_' + str(index) + context["id"] +'" class="main_submit_btn" type="submit" name="send" value="' + main_button_str + '">'
            index += 1

        return """
        
        <form id="%s" action="%s" method="%s" onsubmit="return false;">
            <div class="table_holder">
            <div id="toolbar_%s"></div>
            <table id="table_%s"></table>
            %s
            </div>
        </form>
        
        <script>
            var table_value = %s;
            
            var table_init = {
                "data": {
                    "total": table_value["data"].length,
                    "totalNotFiltered": table_value["data"].length,
                    "rows": table_value["data"]
                },
                "columns": table_value["column"]
            }

            if (table_value["toolbar"]) {
                table_init["toolbar"] = "#toolbar_%s"
                table_init["search"] = true
                table_init["showExport"] = true
                table_init["showColumns"] = true
                table_init["showColumns-toggle-all"] = true
                table_init["showRefresh"] = true
                table_init["showToggle"] = true
                table_init["showFullscreen"] = true
            }

            if (table_value["page_footer"]) {
                table_init["pagination"] = true
                table_init["pageSize"] = table_value["page_footer_detail"]["page_size"]
                table_init["pageList"] = table_value["page_footer_detail"]["page_list"]
                table_init["showFooter"] = true
            }

            if (table_value["page_detail"]) {
                table_init["detailView"] = true
                table_init["detailFormatter"] = detailFormatter
            }

            if (table_value["input_button"] !== "none") {

                var temp = {}
                
                temp["field"] = "state"
                temp[table_value["input_button"]] = true
                temp["rowspan"] = table_value["column"].length
                temp["align"] = "center"
                temp["valign"] = "middle"

                table_init["columns"][0].unshift(temp)
                table_init["idField"] = table_value["input_value_col_field"]
                table_init["selectItemName"] = %s
                        
            }

            function detailFormatter(index, row) {
                if (table_value["page_detail_content"] == "key_value") {

                    var html = []
                    $.each(row, function (key, value) {
                        html.push('<p><b>' + key + ':</b> ' + value + '</p>')
                    })
                    return html.join('')
                }
                
                else {
                    return table_value["page_detail_content"].join('')
                }
            }


            function initTable%s() {
                $('#table_%s').bootstrapTable('destroy').bootstrapTable(table_init)
            }

            $(function() {
                initTable%s()
            })
        </script>
        <script type="text/javascript">
            for(var i=0; i < %s; i++) {
                $('#mb_' + i + '%s').bind('click', (e) => {
                    if (%s) {
                        $('#loading_holder').css("display","flex");
                    }
                    var form_element = document.getElementById('%s')
                    var formData = new FormData(form_element)
                    var response_dict = {}
                    response_dict[e.currentTarget.id] = [e.currentTarget.value]
                    for (var pair of formData.entries()) {
                        if (!(pair[0] in response_dict)) {
                            response_dict[pair[0]] = [pair[1]]
                        }
                        else {
                            response_dict[pair[0]].push(pair[1])
                        }
                    }
                    Sijax.request('update_page', ["%s", "%s", "%s", response_dict]);
                });
            }
        </script>
        <script>%s('%s', %s)</script>
        """ % (context["id"], context["action"], context["method"], context["id"], context["id"], main_button_html, json.dumps(context), context["id"], context["id"], context["id"], context["id"], context["id"], len(context["main_button_name"]), context["id"], context["loader"], context["id"], context["id"], context["action"], context["target_id"], context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return"""
        <!--table-->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
        <link rel="stylesheet" href="https://unpkg.com/bootstrap-table@1.18.3/dist/bootstrap-table.min.css">
        <link href="https://unpkg.com/bootstrap-table@1.18.3/dist/bootstrap-table.min.css" rel="stylesheet">
        <script src="https://unpkg.com/tableexport.jquery.plugin/tableExport.min.js"></script>
        <script src="https://unpkg.com/bootstrap-table@1.18.3/dist/bootstrap-table.min.js"></script>
        <script src="https://unpkg.com/bootstrap-table@1.18.3/dist/bootstrap-table-locale-all.min.js"></script>
        <script src="https://unpkg.com/bootstrap-table@1.18.3/dist/extensions/export/bootstrap-table-export.min.js"></script>
        %s
        """ % (header_script)