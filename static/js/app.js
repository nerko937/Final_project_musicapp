$(function () {
    // article card events
    var cards = $('.card-js');
    if (cards.length !== 0) {
        cards.hover(function () {
            $(this)
                .find('.card-header')
                .removeClass('bg-dark').addClass('bg-info')
        }, function () {
            $(this)
                .find('.card-header')
                .removeClass('bg-info').addClass('bg-dark')
        });
    }
    // Quill
    // new article textarea
    var quillEditor = $('#editor');
    if (quillEditor.length !== 0) {
        var quill = new Quill('#editor', {
            modules: {
                toolbar: [
                    [{ header: [false, 2, 3] }],
                    ['bold', 'italic', 'underline'],
                    ['link', 'blockquote', 'image'],
                    [{ list: 'ordered' }, { list: 'bullet' }]
                ]
            },
            theme: 'snow',
            placeholder: 'Tutaj napisz artykuł.'
        });
        var form = quillEditor.parent();
        var formInput = form.find('#id_content');
        quill.clipboard.dangerouslyPasteHTML(formInput.val());
        form.submit(function (event) {
            event.preventDefault();
            var article = quill.root.innerHTML;
            formInput.val(article);
            $(this).unbind('submit').submit();
        });
    }
    // new song lyrics textarea
    var quillSmallEditor = $('#small-editor');
    if (quillSmallEditor.length !== 0) {
        var quill = new Quill('#small-editor', {
            modules: {
                toolbar: false
            },
            theme: 'snow',
            placeholder: 'Tutaj napisz tekst piosenki.'
        });
        var songForm = quillSmallEditor.parent();
        var songFormInput = songForm.find('#id_lyrics');
        quill.clipboard.dangerouslyPasteHTML(songFormInput.val());
        songForm.submit(function (event) {
            event.preventDefault();
            var song = quill.root.innerHTML;
            songFormInput.val(song);
            $(this).unbind('submit').submit();
        });
    }
    // confirm delete for buttons/links
    var delBtns = $('.del-btn');
    if (delBtns.length !== 0) {
        delBtns.click(function (event) {

            event.preventDefault();

            delUrl = $(this).attr('href');
            confModal = $("#confirmModal");
            confModal.modal('show');

            $("#modalYes").one("click", function(){
                confModal.modal('hide');
                window.location = delUrl
            });

            $("#modalNo").one("click", function(){
                confModal.modal('hide');
            });
        });
    }
    // list items events
    var bandLis = $('.list-group-item-dark');
    var albumLis = $('.list-group-item-secondary');
    var songLis = $('.song-list-item');
    if (bandLis.length !== 0 || albumLis.length !== 0 || songLis.length !== 0) {
        bandLis.hover(function () {
            $(this)
                .css('cursor', 'pointer')
                .removeClass('list-group-item-dark')
                .addClass('list-group-item-primary')
        }, function () {
            $(this)
                .removeClass('list-group-item-primary')
                .addClass('list-group-item-dark')
        });
        bandLis.click(function (event) {
            if (!$(event.target).hasClass('list-icon-redirect')) {
                window.location = 'http://127.0.0.1:8000/band/' + $(this).attr('data-band-id') + '/'
            }
        });
        albumLis.hover(function () {
            $(this)
                .css('cursor', 'pointer')
                .removeClass('list-group-item-secondary')
                .addClass('list-group-item-primary')
        }, function () {
            $(this)
                .removeClass('list-group-item-primary')
                .addClass('list-group-item-secondary')
        });
        albumLis.click(function (event) {
            if (!$(event.target).hasClass('list-icon-redirect')) {
                window.location = 'http://127.0.0.1:8000/album/' + $(this).attr('data-album-id') + '/'
            }
        });
        songLis.hover(function () {
            $(this)
                .css('cursor', 'pointer')
                .addClass('list-group-item-primary')
        }, function () {
            $(this)
                .removeClass('list-group-item-primary')
        });
        songLis.click(function (event) {
            if (!$(event.target).hasClass('list-icon-redirect')) {
                window.location = 'http://127.0.0.1:8000/song/' + $(this).attr('data-song-id') + '/'
            }
        });
    }
    // remove margins for lyrics
    $('.lyrics').parent().addClass('mb-0')
    /*
    // hide/show edit form for author/mod
    var editBtns = $('.edit-btn');
    if (editBtns  !== 0) {
        editBtns.click(function (event) {
            event.preventDefault();

            var card = $(this).parent().next();
            var p = card.find('.card-p-text').hide();
            var form = card.find('.card-form-bg');
            var img = card.find('.cover-img')
            img.fadeOut()

            form
                .show()
                .find('fieldset')
                .prop("disabled", false)
                .submit(function (event) {
                    var pInput = form.find('#id_content').val();
                    p.text = pInput;
                    p.show();
                    img.show();
                })
        });
    }*/
});