$(document).ready(function() {
	$('textarea').autogrow({ onInitialize: true });
	document.getElementById('add_more_skill').addEventListener('click', (e) => {
		element = document.getElementById('id_skill_set-TOTAL_FORMS');
		let id = parseInt(element.value);
		//empty_form = document.getElementById('empty_form')
		list = document.getElementById('circle--clone--list_skill');
        form = document.getElementById('empty_form_skill').cloneNode(true);
        form.removeAttribute('id')
		form.style.display = 'initial';
		for (let i = 0; i < 5; i++) {
			form.children[i].outerHTML = form.children[i].outerHTML.replace(/__prefix__/g, id)
		}

		list.appendChild(form);
		element.value = id + 1;
	});

	document.getElementById('add_more_project').addEventListener('click', (e) => {
		element = document.getElementById('id_skill_set-TOTAL_FORMS');
		let id = parseInt(element.value);
		//empty_form = document.getElementById('empty_form')
		list = document.getElementById('circle--clone--list_project');
		form = document.getElementById('empty_form_project').cloneNode(true);
		form.style.display = 'initial';
		for (e of form.children) {
			if (e.name) {
				e.name.replace('__prefix__', id);
			}
			if (e.id) {
				e.id.replace('__prefix__', id);
			}
		}
		list.appendChild(form);
		element.value = id + 1;
    });
    
    function readURL(input) {
        if (input.files && input.files[0]) {
          var reader = new FileReader();
          
          reader.onload = function(e) {
            $('#blah').attr('src', e.target.result);
          }
          
          reader.readAsDataURL(input.files[0]);
          $("#blah").show()
        }
      }
      
      $("#id_image").change(function() {
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
