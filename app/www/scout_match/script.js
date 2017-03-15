function onceDocumentReady() {
	var scout_match = new Vue({
		el: '#vue-app',
		mounted: function() {
			toast('info', 'Component Mounted', '');
			var self = this;
			self.match_id = $.QueryString.match_id || null;
			if (self.match_id === null) {
				self.match_id = self.generateUUID4();
			}
			toast('info', 'Match ID', self.match_id);
		},
		methods: {
			generateUUID4: function () {
				// src https://gist.github.com/kaizhu256/4482069
				var uuid = '', ii;
				for (ii = 0; ii < 32; ii += 1) {
					switch (ii) {
						case 8:
						case 20:
							uuid += '-';
							uuid += (Math.random() * 16 | 0).toString(16);
							break;
						case 12:
							uuid += '-';
							uuid += '4';
							break;
						case 16:
							uuid += '-';
							uuid += (Math.random() * 4 | 8).toString(16);
							break;
						default:
							uuid += (Math.random() * 16 | 0).toString(16);
					}
				}
				return uuid;
			},
			save: function() {
				var self = this;
				toast('info', 'Saving...', '');
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				matches[self.match_id] = {
					match_id: self.match_id,
					event_name: self.event_name,
					match_number: self.match_number,
					auto_line_cross: self.auto_line_cross,
					auto_low_goal: self.auto_low_goal,
					auto_hopper: self.auto_hopper,
					auto_collect: self.auto_collect,
					auto_gear_pos: self.auto_gear_pos,
					auto_high_goal_pos: self.auto_high_goal_pos,
					climb_rating: self.climb_rating,
					gear_rating: self.gear_rating,
					total_gears: self.total_gears,
					gear_dispense_method: self.gear_dispense_method,
					got_gear_from_human: self.got_gear_from_human,
					got_gear_from_floor: self.got_gear_from_floor,
					high_goal_rating: self.high_goal_rating,
					high_goal_shoot_from_key: self.high_goal_shoot_from_key,
					high_goal_shoot_from_wall: self.high_goal_shoot_from_wall,
					high_goal_shoot_from_afar: self.high_goal_shoot_from_afar,
					low_goal_rating: self.low_goal_rating,
					total_hoppers: self.total_hoppers,
					collected_from_hopper: self.collected_from_hopper
				};
				localStorage.setItem('matches', JSON.stringify(matches));
			}
		},
		data: function() {
			return {
				match_id: 'place510-hold-ere7-uuid-92361f002671',
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
