<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>{{title}}}</title>
    <style>{{!style}}</style>
</head>
<body>
    <div id="content">
        <progress value="0" id="progressBar">
            <div class="progress-container">
                <span class="progress-bar"></span>
            </div>
        </progress>
        %include _html_button_group prev_button=prev_button, next_button=next_button
        <article>
            {{!body}}
        </article>
        %include _html_button_group prev_button=prev_button, next_button=next_button
    </div>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>
        $(document).on('ready', function () {
            var winHeight = $(window).height(),
                docHeight = $(document).height(),
                progressBar = $('progress'),
                max, value;
            max = docHeight - winHeight;
            progressBar.attr('max', max);
            $(document).on('scroll', function () {
                value = $(window).scrollTop();
                progressBar.attr('value', value);
            });
        });
    </script>
</body>
</html>