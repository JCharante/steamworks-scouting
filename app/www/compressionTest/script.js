function onceDocumentReady() {
	var compressionTestPage = new Vue({
		el: '#vue-app',
		mounted: function () {
			var self = this;

			var existing_matches = JSON.parse(localStorage.getItem('matches') || '{}');
			if (Object.keys(existing_matches).length > 0) {
				self.json = existing_matches[Object.keys(existing_matches)[0]];
			} else {
				self.json = {"d5837274-81d9-4745-8ef4-529c90d05a0f":{"match_id":"d5837274-81d9-4745-8ef4-529c90d05a0f","event_name":"practice","match_number":"Q69","auto_line_cross":false,"auto_low_goal":false,"auto_hopper":false,"auto_collect":false,"auto_gear_pos":"none","auto_high_goal_pos":"none","climb_rating":"neutral","gear_rating":"neutral","total_gears":0,"gear_dispense_method":"none","got_gear_from_human":false,"got_gear_from_floor":false,"high_goal_rating":"ds","high_goal_shoot_from_key":false,"high_goal_shoot_from_wall":false,"high_goal_shoot_from_afar":false,"low_goal_rating":"ds","total_hoppers":0,"collected_from_hopper":false}}
			}

			self.compressed_json = JSONC.compress(self.json);
			self.uncompressed_json = JSONC.decompress(self.compressed_json);
			self.packed_json = JSONC.pack(self.json);
			self.unpackedJson = JSONC.unpack(self.packed_json);
			self.lzwString = JSONC.pack(self.json, true);
			self.unpackedLzwString = JSONC.unpack(self.lzwString, true);
		},
		methods: {
			qrCode: function(message) {
				cordova.plugins.barcodeScanner.encode(cordova.plugins.barcodeScanner.Encode.TEXT_TYPE, message, function(success) {
						//alert("encode success: " + success);
						//toast('info', 'Encoding Success', success);
						console.log(success);
					}, function(fail) {
						alert("encoding failed: " + fail);
					}
				);
			}
		},
		data: function() {
			var self = this;
			return {
				json: {},
				compressed_json: '',
				uncompressed_json: {},
				packed_json: '',
				unpackedJson: {},
				lzwString: '',
				unpackedLzwString: {}
			}
		}
	})
}

$(document).ready(onceDocumentReady);