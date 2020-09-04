$(function() {

    // Upload handler from https://stackoverflow.com/a/49024766
    $("form#form_upload_picture").submit(function(event) {
        event.preventDefault();

        var post_data = new FormData($("form")[0]);

        $.ajax({
            xhr: () => {
                var xhr = new window.XMLHttpRequest();
                var new_div = document.createElement('div');

                new_div.innerHTML = '<div class="offset-lg-2"><span id="status"></span> (<span id="loaded_n_total"></span>)<br/><div class="progress"><div class="progress-bar" id="upload-progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div></div></div>';
                document.getElementsByClassName('submit-row')[0].appendChild(new_div)

                xhr.upload.addEventListener("progress", (event) => {
                    _("loaded_n_total").html(formatBytes(event.loaded) + "/" + formatBytes(event.total));
                    var percent = (event.loaded / event.total) * 100;
                    _("status").html(Math.round(percent) + "% uploaded... please wait");
                    updateProgressBar(Math.round(percent));
                }, false);
                xhr.addEventListener("load", () => {
                    _("status").html("Upload successful");
                    updateProgressBar(100);
                }, false);
                xhr.addEventListener("error", () => {_("status").html("Upload failed")}, false);
                xhr.addEventListener("abort", () => {_("status").html("Upload aborted");}, false);

                return xhr;
            },
            url: window.location.href, // to allow add and edit
            type: "POST",
            data: post_data,
            processData: false,
            contentType: false,
            success: function(result) {
                sleep(500).then(() => {window.location.replace("/admin/")});
            }
        });
    });
});

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function formatBytes(bytes, decimals = 2) {
    // From https://stackoverflow.com/a/18650828
    if (bytes === 0) return '0 Bytes';

    const k = 1000; // Set 1024 for real bytes conversion
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

function _(el) {
    return $("#"+el);
}

function updateProgressBar(percentage) {
    _('upload-progress-bar').css('width', percentage+'%');
    _('upload-progress-bar').attr('aria-valuenow', percentage);
}
