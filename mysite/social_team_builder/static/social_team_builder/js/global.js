$(document).ready(function() {
    $('textarea').autogrow({ onInitialize: true });
    
    skill_el = document.getElementById('add_more_skill');
	if (skill_el) {
		skill_el.addEventListener('click', (e) => {
			element = document.getElementById('id_skill_set-TOTAL_FORMS');
			let id = parseInt(element.value);
			//empty_form = document.getElementById('empty_form')
			list = document.getElementById('circle--clone--list_skill');
			form = document.getElementById('empty_form_skill').cloneNode(true);
			form.removeAttribute('id');
			form.style.display = 'initial';
			for (e of form.children) {
				e.outerHTML = e.outerHTML.replace(/__prefix__/g, id);
			}
			list.appendChild(form);
			element.value = id + 1;
		});
	}

	project_el = document.getElementById('add_more_project');
	if (project_el) {
		project_el.addEventListener('click', (e) => {
			element = document.getElementById('id_skill_set-TOTAL_FORMS');
			let id = parseInt(element.value);
			//empty_form = document.getElementById('empty_form')
			list = document.getElementById('circle--clone--list_project');
			form = document.getElementById('empty_form_project').cloneNode(true);
			form.style.display = 'initial';
			for (e of form.children) {
				e.outerHTML = e.outerHTML.replace(/__prefix__/g, id);
			}
			list.appendChild(form);
			element.value = id + 1;
		});
	}

	position_el = document.getElementById('add_more_position');
	if (position_el) {
		position_el.addEventListener('click', (e) => {
			element = document.getElementById('id_positions_set-TOTAL_FORMS');
			let id = parseInt(element.value);
			//empty_form = document.getElementById('empty_form')
			list = document.getElementById('circle--clone--list_position');
			form = document.getElementById('empty_form_position').cloneNode(true);
			form.removeAttribute('id');
			form.style.display = 'list-item';
			for (e of form.children) {
				e.outerHTML = e.outerHTML.replace(/__prefix__/g, id);
			}
			// form.children[4].children[0].src =
			// '/summernote/editor/id_positions_set-__prefix__-description/';
			list.appendChild(form);
            element.value = id + 1;
            // fast solution for summernote - append child does not execute script tag with settings
            let name = `settings_id_positions_set_${id}_description`;
            window[name] = {
                width: '100%',
                height: '200',
                lang: 'en-US',
                toolbar: [
                    ['style', ['style']],
                    [
                        'font',
                        [
                            'bold',
                            'italic',
                            'underline',
                            'superscript',
                            'subscript',
                            'strikethrough',
                            'clear'
                        ]
                    ],
                    ['fontname', ['fontname']],
                    ['fontsize', ['fontsize']],
                    ['color', ['color']],
                    ['para', ['ul', 'ol', 'paragraph']],
                    ['height', ['height']],
                    ['table', ['table']],
                    ['insert', ['link', 'picture', 'video', 'hr']],
                    ['view', ['fullscreen', 'codeview']],
                    ['help', ['help']]
                ],
                url: {
                    language: '/static/summernote/lang/summernote-en-US.min.js',
                    upload_attachment: '/summernote/upload_attachment/'
                }
            };
		});
	}

	function readURL(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();

			reader.onload = function(e) {
				$('#blah').attr('src', e.target.result);
			};

			reader.readAsDataURL(input.files[0]);
			$('#blah').show();
		}
	}

	$('#id_image').change(function() {
		readURL(this);
	});

	//Cloner for infinite input lists
	$('.circle--clone--list').on('click', '.circle--clone--add', function() {
		var parent = $(this).parent('li');
		var copy = parent.clone();
		parent.after(copy);
		copy.find('*:first-child').focus();
	});

	$('.circle--clone--list').on(
		'click',
		'li:not(:only-child) .circle--clone--remove',
		function() {
			var parent = $(this).parent('li');
			parent.remove();
		}
	);

	// Adds class to selected item
	$('.circle--pill--list a').click(function() {
		$('.circle--pill--list a').removeClass('selected');
		$(this).addClass('selected');
	});

	// Adds class to parent div of select menu
	$('.circle--select select')
		.focus(function() {
			$(this)
				.parent()
				.addClass('focus');
		})
		.blur(function() {
			$(this)
				.parent()
				.removeClass('focus');
		});

	// Clickable table row
	$('.clickable-row').click(function() {
		var link = $(this).data('href');
		var target = $(this).data('target');

		if ($(this).attr('data-target')) {
			window.open(link, target);
		} else {
			window.open(link, '_self');
		}
	});

	// Custom File Inputs
	var input = $('.circle--input--file');
	var text = input.data('text');
	var state = input.data('state');
	input.wrap(function() {
		return "<a class='button " + state + "'>" + text + '</div>';
	});
});
