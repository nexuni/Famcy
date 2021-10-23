import json
import Famcy
from flask import current_app

class with_btn_calendar(Famcy.FamcyBlock):
    """
    Represents the block to display
    calendar with buttons. 
    """
    def __init__(self, **kwargs):
        super(with_btn_calendar, self).__init__(**kwargs)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "title": "Selected dates / times:",
            "action_after_post": "save",                    # (clean / save)
            "submit_type": "update_alert",
            "main_button_name": ["送出資料1", "送出資料2"],                                                     # btn name in same section must not be same
            "loader": False,
            "weekdays": ['SUN', 'MON', 'TUE', 'WED', 'THURS', 'FRI', 'SAT'],
            "months": ['JAN', 'FEB', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC'],
            "week_avail": [
                            [
                                ['1:00', '2:00', '3:00', '4:00', '5:00'],
                                ['1:00', '2:00', '3:00', '4:00', '5:00'],
                                ['1:00', '2:00', '3:00', '4:00', '5:00'],
                                ['1:00', '2:00', '3:00', '4:00', '5:00'],
                                ['1:00', '2:00', '3:00', '4:00', '5:00'],
                                ['1:00', '2:00', '3:00', '4:00', '5:00'],
                                ['1:00', '2:00', '3:00', '4:00', '5:00']
                            ],
                            [
                                ['2:00', '5:00'],
                                ['4:00', '5:00', '6:00', '7:00', '8:00'],
                                ['4:00', '5:00'],
                                ['2:00', '5:00'],
                                ['2:00', '5:00'],
                                ['2:00', '5:00'],
                                ['2:00', '5:00']
                            ]
                        ],
            "special_avail_dict": [{
                "year": "2021",
                "month": "SEPT",
                "first_date": "7",
                "mode": 1
            }],
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
        <div id="picker"></div>
        <form id="%s" action="%s" method="%s" onsubmit="return false;">
            <div class="selected_list">
                <p>%s</p>
                <input type="hidden" name="%s" id="picked_time">
                <div id="selected-dates"></div>
            </div>
            %s
        </form>
            
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        <script type="text/javascript">
            var input_calendar_dict = %s;
            (function($) {
                // https://stackoverflow.com/questions/563406/add-days-to-javascript-date
                Date.prototype.addDays = function(days) {
                    var date = new Date(this.valueOf());
                    date.setDate(date.getDate() + days);
                    return date;
                }

                $.fn.markyourcalendar = function(opts) {
                    var prevHtml = `
                        <div id="myc-prev-week">
                            <
                        </div>
                    `;
                    var nextHtml = `<div id="myc-next-week">></div>`;
                    var defaults = {
                        availability: [[], [], [], [], [], [], []], // listahan ng mga oras na pwedeng piliin
                        isMultiple: false,
                        months: input_calendar_dict["months"],
                        prevHtml: prevHtml,
                        nextHtml: nextHtml,
                        selectedDates: [],
                        startDate: new Date(),
                        weekdays: input_calendar_dict["weekdays"],
                    };
                    var settings = $.extend({}, defaults, opts);
                    var html = ``;

                    var onClick = settings.onClick;
                    var onClickNavigator = settings.onClickNavigator;
                    var instance = this;

                    // kuhanin ang buwan
                    this.getMonthName = function(idx) {
                        return settings.months[idx];
                    };

                    var formatDate = function(d) {
                        var date = '' + d.getDate();
                        var month = '' + (d.getMonth() + 1);
                        var year = d.getFullYear();
                        if (date.length < 2) {
                            date = '0' + date;
                        }
                        if (month.length < 2) {
                            month = '0' + month;
                        }
                        return year + '-' + month + '-' + date;
                    };

                    // Eto ang controller para lumipat ng linggo
                    // Controller to change 
                    this.getNavControl = function() {
                        var previousWeekHtml = `<div id="myc-prev-week-container">` + settings.prevHtml + `</div>`;
                        var nextWeekHtml = `<div id="myc-prev-week-container">` + settings.nextHtml + `</div>`;
                        var monthYearHtml = `
                            <div id="myc-current-month-year-container">
                                ` + this.getMonthName(settings.startDate.getMonth()) + ' ' + settings.startDate.getFullYear() + `
                            </div>
                        `;

                        var navHtml = `
                            <div id="myc-nav-container">
                                ` + previousWeekHtml + `
                                ` + monthYearHtml + `
                                ` + nextWeekHtml + `
                                <div style="clear:both;"></div>
                            </div>
                        `;
                        return navHtml;
                    };

                    // kuhanin at ipakita ang mga araw
                    this.getDatesHeader = function() {
                        var tmp = ``;
                        for (i = 0; i < 7; i++) {
                            var d = settings.startDate.addDays(i);
                            tmp += `
                                <div class="myc-date-header" id="myc-date-header-` + i + `">
                                    <div class="myc-date-number">` + d.getDate() + `</div>
                                    <div class="myc-date-display">` + settings.weekdays[d.getDay()] + `</div>
                                </div>
                            `;
                        }
                        var ret = `<div id="myc-dates-container">` + tmp + `</div>`;
                        return ret;
                    }

                    // kuhanin ang mga pwedeng oras sa bawat araw ng kasalukuyang linggo
                    this.getAvailableTimes = function() {
                        var tmp = ``;
                        for (i = 0; i < 7; i++) {
                            var tmpAvailTimes = ``;
                            $.each(settings.availability[i], function() {
                                tmpAvailTimes += `
                                    <a href="javascript:;" class="myc-available-time" data-time="` + this + `" data-date="` + formatDate(settings.startDate.addDays(i)) + `">
                                        ` + this + `
                                    </a>
                                `;
                            });
                            tmp += `
                                <div class="myc-day-time-container" id="myc-day-time-container-` + i + `">
                                    ` + tmpAvailTimes + `
                                    <div style="clear:both;"></div>
                                </div>
                            `;
                        }
                        return tmp
                    }

                    // i-set ang mga oras na pwedeng ilaan
                    this.setAvailability = function(arr) {
                        settings.availability = arr;
                        render();
                    }

                    // clear
                    this.clearAvailability = function() {
                        settings.availability = [[], [], [], [], [], [], []];
                    }

                    // pag napindot ang nakaraang linggo
                    this.on('click', '#myc-prev-week', function() {
                        settings.startDate = settings.startDate.addDays(-7);
                        instance.clearAvailability();
                        render(instance);

                        if ($.isFunction(onClickNavigator)) {
                            onClickNavigator.call(this, ...arguments, instance);
                        }
                    });

                    // pag napindot ang susunod na linggo
                    this.on('click', '#myc-next-week', function() {
                        settings.startDate = settings.startDate.addDays(7);
                        instance.clearAvailability();
                        render(instance);

                        if ($.isFunction(onClickNavigator)) {
                            onClickNavigator.call(this, ...arguments, instance);
                        }
                    });

                    // pag namili ng oras
                    this.on('click', '.myc-available-time', function() {
                        var date = $(this).data('date');
                        var time = $(this).data('time');
                        var tmp = date + ' ' + time;
                        if ($(this).hasClass('selected')) {
                            $(this).removeClass('selected');
                            var idx = settings.selectedDates.indexOf(tmp);
                            if (idx !== -1) {
                                settings.selectedDates.splice(idx, 1);
                            }
                        } else {
                            if (settings.isMultiple) {
                                $(this).addClass('selected');
                                settings.selectedDates.push(tmp);
                            } else {
                                settings.selectedDates.pop();
                                if (!settings.selectedDates.length) {
                                    $('.myc-available-time').removeClass('selected');
                                    $(this).addClass('selected');
                                    settings.selectedDates.push(tmp);
                                }
                            }
                        }
                        if ($.isFunction(onClick)) {
                            onClick.call(this, ...arguments, settings.selectedDates);
                        }
                    });

                    var render = function() {
                        ret = `
                            <div id="myc-container">
                                <div id="myc-nav-container">` + instance.getNavControl() + `</div>
                                <div id="myc-week-container">
                                    <div id="myc-dates-container">` + instance.getDatesHeader() + `</div>
                                    <div id="myc-available-time-container">` + instance.getAvailableTimes() + `</div>
                                </div>
                            </div>
                        `;
                        instance.html(ret);
                    };

                    render();
                };
            })(jQuery);
        

            var special_avail_dict = input_calendar_dict["special_avail_dict"]

            function special_avail(year, month, first_date) {
                for (var i = 0; i < special_avail_dict.length; i++) {
                    if (special_avail_dict[i]["year"] === year && (special_avail_dict[i]["month"] === month || special_avail_dict[i]["month"] === "") && (special_avail_dict[i]["first_date"] === first_date || special_avail_dict[i]["first_date"] === "")) {
                        return special_avail_dict[i]["mode"]
                    }
                }
                return 0
            }

            (function($) {

                if (input_calendar_dict["action_after_post"] === "save") {
                    var temp = ``;
                    var temp_data = getMultSavedValue(input_calendar_dict["id"]);
                    $.each(temp_data, function() {
                        var d = this.split(' ')[0];
                        var t = this.split(' ')[1];
                        temp += `<p>` + d + ` ` + t + `</p>`;
                    });
                    $('#selected-dates').html(temp);
                    document.getElementById("picked_time").value = getMultSavedValue(input_calendar_dict["id"]);
                }
                


                $('#picker').markyourcalendar({
                    availability: input_calendar_dict["week_avail"][0],
                    isMultiple: true,
                    onClick: function(ev, data) {
                        var html = ``;
                        $.each(data, function() {
                            var d = this.split(' ')[0];
                            var t = this.split(' ')[1];
                            html += `<p>` + d + ` ` + t + `</p>`;
                        });
                        $('#selected-dates').html(html);
                        saveMultValue("calendar", data)
                        document.getElementById("picked_time").value = getMultSavedValue(input_calendar_dict["id"])
                    },
                    onClickNavigator: function(ev, instance) {
                        var arr = input_calendar_dict["week_avail"];
                        var year_month = document.getElementById("myc-current-month-year-container").innerText.split(" ")
                        var date = document.getElementsByClassName("myc-date-number")[0].innerText
                        var rn = special_avail(year_month[1], year_month[0], date)
                        instance.setAvailability(arr[rn]);
                    }
                });
            })(jQuery);
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
        """ % (context["id"], context["action"], context["method"], context["title"], context["id"], main_button_html, json.dumps(context), len(context["main_button_name"]), context["id"], context["loader"], context["id"], context["id"], context["action"], context["target_id"], context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return """
        <!--with btn calendar-->
        <link href="https://www.jqueryscript.net/css/jquerysctipttop.css" rel="stylesheet" type="text/css">
        <link rel="stylesheet" type="text/css" href="%s/static/css/mark-your-calendar.css">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/2.1.4/toastr.min.css" rel="stylesheet"  />
        %s
        """ % (current_app.config.get("main_url", ""), header_script)