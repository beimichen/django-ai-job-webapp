$(document).ready(function () {

    function BtnSlider() {
        const slider = document.querySelector('.options');
        let isDown = false;
        let startX;
        let scrollLeft;

        slider.addEventListener('mousedown', (e) => {
            isDown = true;
            slider.classList.add('active');
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        });
        slider.addEventListener('mouseleave', () => {
            isDown = false;
            slider.classList.remove('active');
        });
        slider.addEventListener('mouseup', () => {
            isDown = false;
            slider.classList.remove('active');
        });
        slider.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - slider.offsetLeft;
            const walk = (x - startX) * 3; //scroll-fast
            slider.scrollLeft = scrollLeft - walk;
            console.log(walk);
        });
    }

    jQuery(function ($) {
        var count = 0;

        var firstBotMessage = $('input').attr('data-conv-question');
        console.log(firstBotMessage);

        var messageArray = [];
        var lastMessage = "";

        messageArray.push(firstBotMessage);

        try {
            var url = 'https://' + window.location.host + '/chat/' + senderUUID + '/';
        } catch (err) {
            console.log(err);
        }

        $(".conv-form-wrapper").on('submit', function (e) {
            e.preventDefault();
        });

        var convForm = $('#chat').convform({
            eventList: {
                onInputSubmit: function (convState, ready) {
                    $("#userTextInput").change(function () {
                        if ($(this).closest('form').data('changed')) {
                            console.log('change!');
                        }
                    });

                    var message = convState.current.answer.text;
                    var lastitem = messageArray.length - 1;
                    var list_type_questions = [];
                    var bot_response_after_skip_instruction = "";
                    // var response = "";
                    var flagForSkip = false;

                    console.log(list_type_questions);

                    if (messageArray[lastitem] + 1 > count) {
                        message = $(".userInputDynamic").val();
                    }

                    $.ajax({
                        url: url,
                        type: "POST",
                        dataType: "json",
                        data: {
                            message: message,
                            sender_id: senderUUID,
                            csrfmiddlewaretoken: Cookies.get('csrftoken')
                        },
                        beforeSend: function (jqXHR) {
                            if (lastMessage === "Please sign up first before continuing." || lastMessage === "Okay, come back any time to generate a PDF of your resume! Have a great day :)") {
                                jqXHR.abort();
                            }
                        },
                        success: function (data) {
                            console.log("Successfully sent the data to Django");
                            var bot_response = data.bot_response;
                            var bot_buttons = data.bot_buttons;
                            var list_questions = data.questions_list_type;
                            if (data.questions_list_type !== "none yet" || typeof data.questions_list_type !== 'undefined') {
                                list_type_questions.push(list_questions);
                            }
                            if (list_type_questions.length > 0) {
                                console.log('triggered: ' + list_type_questions[0]);
                                list_type_questions = list_type_questions[0];
                                for (var i = 0; i < list_type_questions.length; i++) {
                                    if (bot_response === list_type_questions[i]) {
                                        var chatForm = $('#convForm');
                                        chatForm.css('display', 'none');
                                        var tagInput = $(".tag-wrapper");
                                        tagInput.appendTo('.card');
                                        tagInput.css('display', 'block');

                                        var tagSubmit = $('.tag-submit');
                                        var tagValuesArray = $('.selectize-input .item').map(
                                            function () {
                                                return $(this).attr('data-value');
                                            }).get();

                                        var textAreaInput = $('#id_tags-selectized');
                                        textAreaInput.click();

                                        tagSubmit.on('click', function () {
                                            var chatInput = $('#userInput');

                                            var tagSelect = $('#id_tags').selectize();
                                            var tagInputElement = tagSelect[0].selectize;

                                            var tagValuesString = tagInputElement.getValue();

                                            tagInputElement.clear();

                                            tagInput.css('display', 'none');
                                            chatForm.css('display', 'block');
                                            chatInput.val(tagValuesString);


                                            var submitBtn = $(".submit");
                                            submitBtn.click();

                                            // var chat = $('#chat');
                                            // chat.submit();
                                        });
                                    } else {
                                        console.log('question_type None triggered')
                                    }
                                }
                            }

                            messageArray.push(message);

                            lastMessage = messageArray[messageArray.length - 1];

                            messageArray.push(data.bot_response);

                            console.log(messageArray);
                            if (convState.current.answer.value === 'end') {
                                convState.current.next = false;
                                //emulating random response time (100-600ms)
                                setTimeout(ready, Math.random() * 500 + 100);
                            } else {
                                if (Array.isArray(convState.current.answer)) var answer = convState.current.answer.join(', ');
                                else var answer = convState.current.answer.text;
                                convState.current.next = true;

                                if (lastMessage === "yes, let me personalize it" || lastMessage === "no, thank you") {
                                    $.ajax({
                                        url: url,
                                        type: "POST",
                                        async: true,
                                        dataType: "JSON",
                                        data: {
                                            chat_basic_complete: 'basic chat complete',
                                            csrfmiddlewaretoken: Cookies.get('csrftoken')
                                        },
                                        success: function (data) {
                                            console.log(data);
                                            console.log('chat_basic_complete');
                                            console.log('flag for success sending last message');
                                        },
                                        error: function (xhr, errmsg, err) {
                                            console.log(xhr.responseText);
                                            console.log(err);
                                            console.log(errmsg);
                                            //console.log("Could not send data to Django. Error: " + xhr.status + ": " + xhr.responseText); #}
                                        }
                                    });
                                }

                                if (bot_response && bot_buttons) {
                                    BtnSlider();
                                    var buttons = [];

                                    function buttonObj() {
                                        for (var i = 0; i < bot_buttons.length; i++) {
                                            bot_buttons[i]['text'] = data.bot_buttons[i]['title'];
                                            delete bot_buttons[i]['title'];
                                            bot_buttons[i]['value'] = bot_buttons[i]['payload'];
                                            delete bot_buttons[i]['payload'];
                                            buttons.push(bot_buttons[i]);
                                        }
                                        console.log(bot_buttons);
                                    }

                                    buttonObj();

                                    console.log('flag for bot buttons');
                                    if (buttons.length > 2) {
                                        convState.current.next = convState.newState({
                                            type: 'select',
                                            name: 'dynamic-question-' + count,
                                            questions: [bot_response],
                                            multiple: true,
                                            answers: buttons
                                        });
                                    } else {
                                        convState.current.next = convState.newState({
                                            type: 'select',
                                            name: 'dynamic-question-' + count,
                                            questions: [bot_response],
                                            answers: buttons
                                        });
                                    }
                                    console.log(bot_response);
                                } else if (bot_response && !bot_buttons) {
                                    if (data.bot_response === "Please sign up or log in first before continuing.") {
                                        var signUpBtn = $("#nav-signup-btn");
                                        signUpBtn.addClass("signup-btn hero-btn animated shake").css("color", "white").click();
                                        $('.submit').hide();
                                        var textArea = $("textarea");
                                        textArea.prop('disabled', true).attr("placeholder", "Please sign up first");
                                        $.ajax({
                                            url: url,
                                            type: "POST",
                                            dataType: "JSON",
                                            async: true,
                                            data: {
                                                chat_basic_complete: 'complete',
                                                csrfmiddlewaretoken: Cookies.get('csrftoken')
                                            },
                                            success: function (data) {
                                                messageArray = [];
                                                console.log(data);
                                                console.log('flag for success sending last message');
                                            },
                                            error: function (xhr, errmsg, err) {
                                                console.log(xhr.responseText);
                                                console.log(err);
                                                console.log(errmsg);
                                                //console.log("Could not send data to Django. Error: " + xhr.status + ": " + xhr.responseText); #}
                                            }
                                        });
                                        // convState.current.next = false;
                                    } else if (data.bot_response === "Okay, come back any time to generate a PDF of your resume! Have a great day :)") {
                                        console.log('flag for last message for basic chat');
                                        $.ajax({
                                            url: url,
                                            type: "POST",
                                            async: true,
                                            dataType: "JSON",
                                            data: {
                                                chat_basic_complete: 'complete without signup or login',
                                                csrfmiddlewaretoken: Cookies.get('csrftoken')
                                            },
                                            success: function (data) {
                                                console.log(data);
                                                console.log('flag for success sending last message');
                                                $('.submit').hide();
                                                var textArea = $("textarea");
                                                textArea.prop('disabled', true).attr("placeholder", "");
                                            },
                                            error: function (xhr, errmsg, err) {
                                                console.log(xhr.responseText);
                                                console.log(err);
                                                console.log(errmsg);
                                                //console.log("Could not send data to Django. Error: " + xhr.status + ": " + xhr.responseText); #}
                                            }
                                        });
                                        convState.current.next = false;
                                        lastMessage = data.bot_response;
                                    } else if (data.bot_response.indexOf("I've created your cover letter") !== -1) {
                                        console.log('flag for last message for full chat');
                                        $.ajax({
                                            url: url,
                                            type: "POST",
                                            async: true,
                                            dataType: "JSON",
                                            data: {
                                                chat_full_complete: 'chat fully complete',
                                                csrfmiddlewaretoken: Cookies.get('csrftoken')
                                            },
                                            success: function (data) {
                                                console.log(data);
                                                console.log('flag for success sending last message');
                                                $('.submit').hide();
                                                var textArea = $("textarea");
                                                textArea.prop('disabled', true).attr("placeholder", "");
                                                setTimeout(function () {

                                                    var messageCheckForLink = $('div.conv-form-wrapper div#messages div.message.to').last().text();

                                                    if (messageCheckForLink.indexOf("I've created your cover letter") !== -1) {
                                                        $('div.conv-form-wrapper div#messages div.message.to').last().linkify();
                                                    }
                                                    console.log('triggered message check for link')

                                                }, 900);
                                                setTimeout(function () {
                                                        Swal.fire({
                                                            title: "Great!",
                                                            html: 'You can go to your ' +
                                                            '<a href="https://YOUR_APP_HOST/dashboard/">dashboard</a> ' +
                                                            ' to further improve your cover letter.',
                                                            type: 'info',
                                                            showCancelButton: true,
                                                            confirmButtonColor: '#3085d6',
                                                            cancelButtonColor: '#d33',
                                                            confirmButtonText: 'Okay',
                                                        })
                                                    }
                                                    , 2200)
                                                //TODO: redirect to dashboard from here in the frontend?
                                            },
                                            error: function (xhr, errmsg, err) {
                                                console.log(xhr.responseText);
                                                console.log(err);
                                                console.log(errmsg);
                                                //console.log("Could not send data to Django. Error: " + xhr.status + ": " + xhr.responseText); #}
                                            }
                                        });
                                        // convState.current.next = false;
                                        lastMessage = data.bot_response;
                                    } else if (data.bot_response === "Something went wrong. Please start a new chat." || data.bot_response === "Sorry but currently I don't support that position." || data.bot_response === "Unfortunately, at the moment, I don't write for that position.") {
                                        $.ajax({
                                            url: url,
                                            type: "POST",
                                            dataType: "JSON",
                                            async: true,
                                            data: {
                                                chat_basic_complete: 'complete',
                                                csrfmiddlewaretoken: Cookies.get('csrftoken')
                                            },
                                            success: function (data) {
                                                messageArray = [];
                                                console.log(data);
                                                console.log('flag for success sending last message');
                                                $('.submit').hide();
                                                var textArea = $("textarea");
                                                textArea.prop('disabled', true).attr("placeholder", "");
                                                console.log('unsupported position');
                                            },
                                            error: function (xhr, errmsg, err) {
                                                console.log(xhr.responseText);
                                                console.log(err);
                                                console.log(errmsg);
                                                //console.log("Could not send data to Django. Error: " + xhr.status + ": " + xhr.responseText); #}
                                            }
                                        });
                                        convState.current.next = false;
                                    } else if (data.bot_response === "Please type 'skip' if you don't want to answer any of the questions I'm about to ask you.") {
                                        $.ajax({
                                            url: url,
                                            type: "POST",
                                            dataType: "JSON",
                                            async: false,
                                            data: {
                                                message: '/inform_go_onto_questions',
                                                csrfmiddlewaretoken: Cookies.get('csrftoken')
                                            },
                                            success: function (_data) {
                                                bot_response_after_skip_instruction = _data.bot_response;
                                                flagForSkip = true;
                                                messageArray.push(_data.bot_response);
                                            },
                                            error: function (xhr, errmsg, err) {
                                                console.log(xhr.responseText);
                                                console.log(err);
                                                console.log(errmsg);
                                                //console.log("Could not send data to Django. Error: " + xhr.status + ": " + xhr.responseText); #}
                                            }
                                        });
                                        console.log(bot_response_after_skip_instruction);
                                    }
                                    console.log('flag for bot response');
                                    convState.current.next = convState.newState({
                                        type: 'text',
                                        noAnswer: true,
                                        name: 'dynamic-question-' + count,
                                        questions: [bot_response]
                                    });
                                    if (flagForSkip === true) {
                                        convState.current.next.next = convState.newState({
                                            type: 'text',
                                            noAnswer: true,
                                            name: 'dynamic-question-' + count,
                                            questions: [bot_response_after_skip_instruction]
                                        });
                                    }
                                }
                                //emulating random response time (100-600ms)
                                setTimeout(ready, Math.random() * 500);
                            }
                            count++;
                        },
                        error: function (xhr, errmsg, err) {
                            //console.log("Could not send data to Django. Error: " + xhr.status + ": " + xhr.responseText); #}
                        }
                    })
                }
            }
        });
        var message = convForm.get;
        console.log('input is being submitted...');
    })
});
