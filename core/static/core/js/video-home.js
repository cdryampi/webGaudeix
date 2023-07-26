document.addEventListener("DOMContentLoaded", function () {
    var youtubeIframe = document.getElementById("_youtube-iframe");
    if (youtubeIframe) {
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        var firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        var youtubePlayer;

        function onYouTubeIframeAPIReady() {
            var playerElement = document.getElementById("_youtube-iframe");
            var youtubeUrl = playerElement.getAttribute("data-youtubeurl");
            youtubePlayer = new YT.Player(playerElement.id, {
                videoId: getYoutubeVideoId(youtubeUrl),
                playerVars: {
                    cc_load_policy: 0,
                    controls: 0,
                    disablekb: 0,
                    iv_load_policy: 3,
                    playsinline: 1,
                    rel: 0,
                    showinfo: 0,
                    modestbranding: 1,
                    autoplay: 1,
                    loop: 1,
                    rel: 0,
                    mute: 1,
                    fs: 0,
                    disablePictureInPicture: true
                },
                events: {
                    'onReady': onYoutubePlayerReady,
                    'onStateChange': onYoutubePlayerStateChange
                }
            });
        }

        function getYoutubeVideoId(youtubeUrl) {
            var videoId;
            var youtubeRegex = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:embed\/|watch\?v=|watch\?.+&v=|v\/)|youtu\.be\/)([^&?/]+)/;
            var match = youtubeUrl.match(youtubeRegex);

            if (match && match[1]) {
                videoId = match[1];
            }

            return videoId;
        }

        function onYoutubePlayerReady(event) {
            event.target.playVideo();
        }

        function onYoutubePlayerStateChange(event) {
            if (event.data == YT.PlayerState.PLAYING) {
                // fade out #_buffering-background
                Velocity(document.getElementById('_buffering-background'), { opacity: 0 }, 500);
            }
            if (event.data == YT.PlayerState.ENDED) {
                event.target.seekTo(0);
            }
        }

        // Llamar a la función onYouTubeIframeAPIReady cuando la API de YouTube esté lista
        window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
    }
});
