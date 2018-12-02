<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1"/>
    <title>{{title}}}</title>
    <style>{{!style}}</style>
    <script>
        window.addEventListener('scroll', function (e) {
            try {
                var scroll = window.scrollY;
                var height = document.body.scrollHeight - window.innerHeight + 10;
                var percent = Math.round(100.0 * scroll / height);
                document.getElementById('readpos').innerText = percent + '%';
            } catch (err) {
                // ignore
            }
        })
    </script>
</head>
<body>
    <div id="content">
        %include _html_button_group prev_button=prev_button, next_button=next_button

        <main>{{!body}}</main>

        %include _html_button_group prev_button=prev_button, next_button=next_button
    </div>
    <div id="readpos">0%</div>
</body>
</html>