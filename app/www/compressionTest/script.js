/*
console.log('Original JSON Size:', JSON.stringify(json).length);
var compressed = JSONC.compress(json);
console.log('Compressed JSON Size (compress):', JSON.stringify(compressed).length);
var uncompressed = JSONC.decompress(compressed);
console.log('Decompressed JSON Size (decompress):', JSON.stringify(uncompressed).length);
var gzip_string = JSONC.pack(json);
console.log('Compressed JSON Size (pack):', gzip_string.length);
var unpacked_gzip_string = JSONC.unpack(gzip_string);
console.log('Decompressed JSON Size (unpack):', JSON.stringify(unpacked_gzip_string).length);
var lzwString = JSONC.pack(json, true);
console.log('Compress JSON (pack, true):', lzwString.length);
var unpacked_lzwString = JSONC.unpack(lzwString, true);
console.log('Decompressed JSON (unpack, true):', JSON.stringify(unpacked_lzwString).length);
*/

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