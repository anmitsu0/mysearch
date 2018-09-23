こんにちは。<b>{{name}}</b>さん。<br/>
<br/>
indexへのリンクテスト<br/>
<a href="{{url('index')}}">hello</a><br/>
<br/>
{{count}}回ループするよ<br/>
<br/>

%for i in range(count):
{{i}}回<br/>
%end

<img src="{{url('static_file', filepath="image.jpg")}}">
