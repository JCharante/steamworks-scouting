function onceDocumentReady() {
	var scout_match = new Vue({
		el: '#vue-app',
		methods: {
		},
		data: function() {
			return {
				event_name: 'practice',
				team_number: 5687,
				match_number: 'Q69',
				auto_line_cross: false,
				auto_low_goal: false,
				auto_hopper: false,
				auto_collect: false,
				auto_gear_pos: 'none',
				auto_high_goal_pos: 'none',
				climb_rating: 'neutral',
				gear_rating: 'neutral',
				total_gears: 0,
				gear_dispense_method: 'none',
				got_gear_from_human: false,
				got_gear_from_floor: false,
				high_goal_rating: 'ds',
				high_goal_shoot_from_key: false,
				high_goal_shoot_from_wall: false,
				high_goal_shoot_from_afar: false,
				low_goal_rating: 'ds',
				total_hoppers: 0,
				collected_from_hopper: false
			}
		}
	})
}

$(document).ready(onceDocumentReady);
