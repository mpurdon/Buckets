window.bucket = window.bucket || {};

/**
 * The main bucket list javascript application
 */
bucket = function() {
	return {
		focusForm : function() {
			$(":input.focus[value=]:first").focus();
		},

		init : function() {
			bucket.search.init();
			bucket.focusForm();
			bucket.rate.init();
			bucket.link.init();
			bucket.ajax.init();
			bucket.kill.init();
		},

		setTimezone : function() {
			var now = new Date();
			var time = now.getTimezoneOffset() / -60;
			$.post('/ajax/set-timezone', {
				offset : time
			});
		}
	};
}();

/**
 * Special handling for links
 */
bucket.link = function() {
	var externalLink = function(e) {
		$(this).attr("target", "_blank");
	};

	var hidePostInstructions = function(e) {
		e.preventDefault();
		var postInstructions = $(this).parents(".postInstructions");
		$.post('/ajax/hide-post-instructions', {
			hide : 1
		}, function(data) {
			if (data.success == 1) {
				postInstructions.fadeOut(200);
			}
		}, "json");
	};

	var toggleFormInstructions = function(e) {
		e.preventDefault();
		$(".formInstructions").slideToggle();
	};

	return {
		init : function() {
			$("a[rel='external']").live("click", externalLink);
			$(".postInstructions > a.hide").live("click", hidePostInstructions);
			$("a.toggleFormInstructions").live("click", toggleFormInstructions);
		}
	}
}();

/**
 * Handle the search box
 */
bucket.search = function() {
	var clearedText = [];

	function clearText() {
		var value = $(this).val();
		var name = $(this).attr("name");
		if (clearedText[name] == undefined) {
			clearedText[name] = value;
		}

		if (value == clearedText[name]) {
			$(this).val("");
		}
	}

	function restoreText() {
		var name = $(this).attr("name");
		if (this.value == "") {
			$(this).val(clearedText[name]);
		}
	}

	return {
		init : function() {
			$("input.clearDefault").focus(clearText);
			$("input.clearDefault").blur(restoreText);
		}
	};
}();

bucket.rate = function() {
	var over = function() {
		$(".percent_rating").hide();
		$(".num_ratings").show();
	};

	var out = function() {
		$(".num_ratings").hide();
		$(".percent_rating").show();
	};

	var handleClick = function(e) {
		e.preventDefault();
		var hot = $(this).hasClass("hot");
		var eventId = $(this).attr("rel");

		var rateDiv = $(this).parents(".rate");
		rateDiv.html('');
		rateDiv.addClass("loading");
		$.post("/ajax/rate", {
			eventId : eventId,
			hot : hot
		}, function(result) {
			rateDiv.removeClass("loading");
			rateDiv.html('<p class="result">' + result.message + '</p>');

			if (!result.ratingChanged) {
				return;
			}

			rating = $(".rating");
			$(".num_ratings", rating).text(result.newCount);
			$(".percent_rating", rating).html(
					result.newRating + '<span>%</span>');
			rating.removeClass(result.oldClass);
			rating.addClass(result.newClass);
		}, "json");
	};

	return {
		init : function() {
			$("a.rate").live("click", handleClick);
			$(".rating").hover(over, out);
		}
	}
}();

bucket.ajax = function() {
	var handleClick = function(e) {
		e.preventDefault();
		var sort = $(this).parents(".sort");
		$("a", sort).removeClass("selected");
		$(this).toggleClass("selected");
		var hash = this.href.replace(wwwUrl, '');
		hash = hash.replace(/^.*#/, '');
		$.historyLoad(hash);
	};

	return {
		init : function() {
			$("a[rel='ajax']").live("click", handleClick);
		}
	}
}();

bucket.kill = function() {
	var show = function(e) {
		e.preventDefault();
		bucket.kill.closeAll();
		var editDiv = $(this).parents(".edit");
		var deleteDiv = $(".delete", editDiv);
		deleteDiv.fadeIn(200);
	};

	var confirm = function(e) {
		e.preventDefault();
		var bits = $(this).attr("rel").split(':');
		$.post("/" + bits[0] + "/delete", {
			id : bits[1]
		}, function(data) {
			if (data.success) {
				window.location = data.redirect;
			}
		}, "json");
	};

	return {
		closeAll : function(e) {
			if (e) {
				e.preventDefault();
			}
			$(".delete").fadeOut(200);
		},

		init : function() {
			$(".showDeleteDialogue").live("click", show);
			$(".deleteCancel").live("click", this.closeAll);
			$(".deleteConfirm").live("click", confirm);

		}
	}
}();

$(document).ready(bucket.init);
