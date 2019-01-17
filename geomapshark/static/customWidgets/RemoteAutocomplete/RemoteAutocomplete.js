(function() {
    function RemoteAutocompleteField(textinput) {
        var countDisplay = document.getElementById(textinput.id + "_counter");
        var countDown = false;
        var minCount, maxCount;
        if (textarea != null && countDisplay != null) {
            minCount = textarea.getAttribute("data-min-count");
            maxCount = textarea.getAttribute("data-max-count");

            Countable.on(textarea, updateFieldWordCount);
        }

        function updateFieldWordCount(counter) {
            var count = counter["words"];
            countDisplay.getElementsByClassName("text-count-current")[0].innerHTML = count;
            if (minCount && count < minCount)
                countDisplay.className = "text-count text-is-under-min";
            else if (maxCount && count > maxCount)
                countDisplay.className = "text-count text-is-over-max";
            else
                countDisplay.className = "text-count";
        }
    }

    document.addEventListener('DOMContentLoaded', function(e) {
        ;[].forEach.call(document.querySelectorAll('[data-count]'), RemoteAutocompleteField)
    })
})()
