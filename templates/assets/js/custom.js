$(document).ready(function() {
    $('a[href^="http"]')
        .attr('target', '_blank');

    var caps = [
        '<em>Vibrio cholerae</em> colonies on an agar plate',
        'Gel shift assay of a cell extract',
        'Mouse embryonic stem cells growing on fibroblasts',
        'Proliferating <em>Macrostomum lignano</em> neoblasts',
        'Donal, my cat :)'
    ];

    var counter = 0;
    $('#intro figure img').click(function() {
        var src = $(this).attr('src');
        var idx = ++counter % caps.length;
        $(this).attr('src', '/img/intro-0' + (idx + 1) + '.jpg');
        $('#intro figure figcaption').html(caps[idx]);
    });
});
