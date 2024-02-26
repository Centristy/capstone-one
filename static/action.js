let text = []




$(document).ready(function() {

    $(".flashcards").click(function(){
        $(this).children(".korean").toggle("slow", function(){})
        })

    $('input[name="korean"]').click(function(){

        text = $('input[name="english"]')[1].value
        
        let apiUrl = `https://api.mymemory.translated.net/get?q=${text}!&langpair=en|ko`
        fetch(apiUrl).then(res => res.json()).then(data=> {

            $('input[name="korean"]')[1].value = data.responseData.translatedText;
        })


        })
    
    });