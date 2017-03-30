function onceDocumentReady() {
	var scout_match = new Vue({
		el: '#vue-app',
		mounted: function() {
			var self = this;
			self.match_id = $.QueryString.match_id || null;
			if (self.match_id === null) {
				self.match_id = self.generateUUID4();
			} else {
				self.loadSavedData();
			}
			console.log('info', 'Match ID:', self.match_id);
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

				if (self.notes.length > 200) {
					playFieldFault();
					toast('error', 'Match Not Saved', 'Notes too Long!');
					return null;
				}

				self.last_modified = new Date().toJSON();
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				matches[self.match_id] = {
					match_id: self.match_id,
					event_name: self.event_name,
					team_number: self.team_number,
					match_number: self.match_number,
					auto_line_cross: self.auto_line_cross,
					auto_low_goal: self.auto_low_goal,
					auto_hopper: self.auto_hopper,
					auto_collect: self.auto_collect,
					auto_gear_pos: self.auto_gear_pos,
					auto_kpa: self.auto_kpa,
					auto_high_goal_pos: self.auto_high_goal_pos,
					climb_rating: self.climb_rating,
					gear_rating: self.gear_rating,
					total_gears: self.total_gears,
					total_kpa: self.total_kpa,
					gear_dispense_method: self.gear_dispense_method,
					got_gear_from_human: self.got_gear_from_human,
					got_gear_from_floor: self.got_gear_from_floor,
					high_goal_rating: self.high_goal_rating,
					high_goal_shoot_from_key: self.high_goal_shoot_from_key,
					high_goal_shoot_from_wall: self.high_goal_shoot_from_wall,
					high_goal_shoot_from_afar: self.high_goal_shoot_from_afar,
					low_goal_rating: self.low_goal_rating,
					total_hoppers: self.total_hoppers,
					collected_from_hopper: self.collected_from_hopper,
					collected_fuel_from_floor: self.collected_fuel_from_floor,
					last_modified: self.last_modified,
					notes: self.notes
				};
				localStorage.setItem('matches', JSON.stringify(matches));
				toast('success', 'Match Saved', '');
			},
			loadSavedData: function () {
				var self = this;
				var matches = JSON.parse(localStorage.getItem('matches') || '{}');
				if (self.match_id in matches) {
					toast('info', 'Loading Previous Data', '');
					var match = matches[self.match_id];
					self.event_name = match.event_name;
					self.team_number = match.team_number;
					self.match_number = match.match_number;
					self.auto_line_cross = match.auto_line_cross;
					self.auto_low_goal = match.auto_low_goal;
					self.auto_hopper = match.auto_hopper;
					self.auto_collect = match.auto_collect;
					self.auto_gear_pos = match.auto_gear_pos;
					self.auto_kpa = match.auto_kpa;
					self.auto_high_goal_pos = match.auto_high_goal_pos;
					self.climb_rating = match.climb_rating;
					self.gear_rating = match.gear_rating;
					self.total_gears = match.total_gears;
					self.total_kpa = match.total_kpa;
					self.gear_dispense_method = match.gear_dispense_method;
					self.got_gear_from_human = match.got_gear_from_human;
					self.got_gear_from_floor = match.got_gear_from_floor;
					self.high_goal_rating = match.high_goal_rating;
					self.high_goal_shoot_from_key = match.high_goal_shoot_from_key;
					self.high_goal_shoot_from_wall = match.high_goal_shoot_from_wall;
					self.high_goal_shoot_from_afar = match.high_goal_shoot_from_afar;
					self.low_goal_rating = match.low_goal_rating;
					self.total_hoppers = match.total_hoppers;
					self.collected_from_hopper = match.collected_from_hopper;
					self.collected_fuel_from_floor = match.collected_fuel_from_floor;
					self.last_modified = match.last_modified;
					self.notes = match.notes;
				}
			}
		},
		data: function() {
			return {
				match_id: 'place510-hold-ere7-uuid-92361f002671',
				event_name: 'practice',
				team_number: null,
				match_number: null,
				auto_line_cross: false,
				auto_low_goal: false,
				auto_hopper: false,
				auto_collect: false,
				auto_gear_pos: 'none',
				auto_kpa: 0,
				auto_high_goal_pos: 'none',
				climb_rating: 'neutral',
				gear_rating: 'neutral',
				total_gears: 0,
				total_kpa: 0,
				gear_dispense_method: 'none',
				got_gear_from_human: false,
				got_gear_from_floor: false,
				high_goal_rating: 'ds',
				high_goal_shoot_from_key: false,
				high_goal_shoot_from_wall: false,
				high_goal_shoot_from_afar: false,
				low_goal_rating: 'ds',
				total_hoppers: 0,
				collected_from_hopper: false,
				collected_fuel_from_floor: false,
				last_modified: "2017-03-17T00:34:15.415Z",
				notes: ''
			}
		}
	})
}

$(document).ready(onceDocumentReady);
