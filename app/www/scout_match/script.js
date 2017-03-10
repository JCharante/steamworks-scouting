function onceDocumentReady() {
	var scout_match = new Vue({
		el: '#vue-app',
		methods: {
		},
		data: function() {
			return {
				event_name: 'practice',
				team_number: 5687,
				match_number: 13,
				auto_line_cross: false,
				auto_low_goal: false,
				auto_hopper: false,
				auto_collect: false,
				auto_gear_pos: 'none',
				auto_high_goal: 'none'
			}
		}
	})
}

$(document).ready(onceDocumentReady);
