window.bucket = window.bucket || {};

bucket.view = {
	init: function() {
		
	},

	showAddBox: function(e) {
		e.preventDefault();
		
		$("#addBoxContainer").dafeIn(500);
		bucket.focusForm();
	},
	
	focusForm: function() {
		
	}
}

$(document).ready(bucket.view.init);
