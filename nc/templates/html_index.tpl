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
        <h2>{{title}}</h2>
        <ul class="chapters">
        %for chapter in chapters:
            <li>
                <a href="{{chapter['link']}}">{{chapter['title']}}</a>
            </li>
        %end
        </ul>
    </div>
</body>
</html>