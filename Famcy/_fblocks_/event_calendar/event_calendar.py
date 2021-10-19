import json
import Famcy
from flask import current_app

class event_calendar(Famcy.FamcyBlock):
    """
    Represents the block to display
    event_calendar. 
    """
    def __init__(self, **kwargs):
        super(event_calendar, self).__init__(**kwargs)

    @classmethod
    def generate_template_content(cls, fblock_type=None):
        """
        This is the function that
        returns the template content 
        for the given fblock. 
        - Return a content dictionary
        """
        return {
            "language": "zh-TW",                                # ("zh-TW" / "en")
            "events": [
                        {
                            "title": 'Repeating Event',
                            "start": "Wed Jul 21 2021 08:00:00 GMT+0800",
                            "allDay": False,
                            "className": 'info'
                        },
                        {
                            "title": 'Meeting',
                            "start": "Wed Jul 21 2021 08:00:00 GMT+0800",
                            "allDay": False,
                            "className": 'important'
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

        if context["language"] == "zh-TW":
            prompt_msg = "請加入活動名稱:"
            language_script = '<script src="' + current_app.config.get("main_url", "") + '/static/js/fullcalendar_zh.js" type="text/javascript"></script>'
        else:
            prompt_msg = "Event Title:"
            language_script = '<script src="' + current_app.config.get("main_url", "") + '/static/js/fullcalendar.js" type="text/javascript"></script>'

        return """
        %s
        <script>
            var event_calendar_dict = %s;

            $(document).ready(function() {
                var date = new Date();
                var d = date.getDate();
                var m = date.getMonth();
                var y = date.getFullYear();

                /*  className colors

                className: default(transparent), important(red), chill(pink), success(green), info(blue)

                */


                /* initialize the external events
                -----------------------------------------------------------------*/

                $('#external-events div.external-event').each(function() {

                    // create an Event Object (http://arshaw.com/fullcalendar/docs/event_data/Event_Object/)
                    // it doesn't need to have a start or end
                    var eventObject = {
                        title: $.trim($(this).text()) // use the element's text as the event title
                    };

                    // store the Event Object in the DOM element so we can get to it later
                    $(this).data('eventObject', eventObject);

                    // make the event draggable using jQuery UI
                    $(this).draggable({
                        zIndex: 999,
                        revert: true,      // will cause the event to go back to its
                        revertDuration: 0  //  original position after the drag
                    });

                });


                /* initialize the calendar
                -----------------------------------------------------------------*/

                var calendar =  $('#calendar').fullCalendar({
                    header: {
                        left: 'title',
                        center: 'agendaDay,agendaWeek,month',
                        right: 'prev,next today'
                    },
                    editable: true,
                    firstDay: 0, //  1(Monday) this can be changed to 0(Sunday) for the USA system
                    selectable: true,
                    defaultView: 'month',

                    axisFormat: 'h:mm',
                    columnFormat: {
                        month: 'ddd',    // Mon
                        week: 'ddd d', // Mon 7
                        day: 'dddd M/d',  // Monday 9/7
                        agendaDay: 'dddd d'
                    },
                    titleFormat: {
                        month: 'MMMM yyyy', // September 2009
                        week: "MMMM yyyy", // September 2009
                        day: 'MMMM yyyy'                  // Tuesday, Sep 8, 2009
                    },
                    allDaySlot: false,
                    selectHelper: true,
                    select: function(start, end, allDay) {
                        var title = prompt("%s");

                        if (title) {
                            calendar.fullCalendar('renderEvent',
                                {
                                    title: title,
                                    start: start,
                                    end: end,
                                    allDay: allDay,
                                    className: "info"
                                }
                            );
                        }
                        calendar.fullCalendar('unselect');
                    },
                    droppable: true, // this allows things to be dropped onto the calendar !!!
                    drop: function(date, allDay) { // this function is called when something is dropped

                        // retrieve the dropped element's stored Event Object
                        var originalEventObject = $(this).data('eventObject');

                        // we need to copy it, so that multiple events don't have a reference to the same object
                        var copiedEventObject = $.extend({}, originalEventObject);

                        // assign it the date that was reported
                        copiedEventObject.start = date;
                        copiedEventObject.allDay = allDay;

                        // render the event on the calendar
                        // the last `true` argument determines if the event "sticks" (http://arshaw.com/fullcalendar/docs/event_rendering/renderEvent/)
                        $('#calendar').fullCalendar('renderEvent', copiedEventObject, true);

                        // is the "remove after drop" checkbox checked?
                        if ($('#drop-remove').is(':checked')) {
                            // if so, remove the element from the "Draggable Events" list
                            $(this).remove();
                        }

                    },

                    events: event_calendar_dict["events"],
                });


            });

        </script>
        <style>

        </style>
        <div id='wrap'>
            <div id='calendar'></div>
        </div>

        <script>%s('%s', %s)</script>

        """ % (language_script, json.dumps(context), prompt_msg, context["js_after_func_name"], context["id"], json.dumps(context["js_after_func_dict"]))

    def extra_script(self, header_script, **configs):
        return header_script